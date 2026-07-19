from __future__ import annotations

import base64
import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from app.config import Settings
from app.server import AppServer, RateLimiter
from tests.helpers import SAMPLE_CV_PARAGRAPHS, SAMPLE_JOB, make_docx


class ServerFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        settings = Settings(
            host="127.0.0.1",
            port=0,
            environment="test",
            app_secret="test-secret",
            database_path=Path(self.temp.name) / "app.db",
            session_ttl_minutes=60,
            max_upload_bytes=5_242_880,
            max_job_description_chars=30_000,
            openai_api_key=None,
            openai_api_base="https://api.openai.com/v1",
            openai_model="gpt-5.6-luna",
            openai_timeout_seconds=5,
        )
        self.server = AppServer(("127.0.0.1", 0), settings)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]
        self.cookie = ""
        self.csrf = ""

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, method: str, path: str, payload=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        headers = {}
        body = None
        if self.cookie:
            headers["Cookie"] = self.cookie
        if payload is not None:
            body = json.dumps(payload)
            headers["Content-Type"] = "application/json"
        if method in {"POST", "DELETE"} and self.csrf:
            headers["X-CSRF-Token"] = self.csrf
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        data = response.read()
        set_cookie = response.getheader("Set-Cookie")
        if set_cookie:
            self.cookie = set_cookie.split(";", 1)[0]
        content_type = response.getheader("Content-Type", "")
        parsed = json.loads(data.decode("utf-8")) if "application/json" in content_type else data
        connection.close()
        return response.status, parsed, response.getheaders()

    def initialize_session(self):
        status, payload, _ = self.request("GET", "/api/session")
        self.assertEqual(status, 200)
        self.csrf = payload["csrf_token"]
        return payload

    def test_full_flow_requires_yes_before_optimization(self) -> None:
        session = self.initialize_session()
        self.assertEqual(session["ai_mode"], "local")
        cv_data = base64.b64encode(make_docx(SAMPLE_CV_PARAGRAPHS)).decode("ascii")
        status, cv_payload, _ = self.request("POST", "/api/cv", {"filename": "resume.docx", "data_base64": cv_data})
        self.assertEqual(status, 201)
        status, job_payload, _ = self.request("POST", "/api/job", {"text": SAMPLE_JOB})
        self.assertEqual(status, 201)
        status, analysis_payload, _ = self.request(
            "POST",
            "/api/analyze",
            {"cv_id": cv_payload["cv"]["id"], "job_id": job_payload["job"]["id"]},
        )
        self.assertEqual(status, 201)
        analysis_id = analysis_payload["analysis"]["id"]

        status, _, _ = self.request("POST", "/api/decision", {"analysis_id": analysis_id, "choice": "no"})
        self.assertEqual(status, 200)
        status, denied, _ = self.request("POST", "/api/optimize", {"analysis_id": analysis_id})
        self.assertEqual(status, 403)
        self.assertIn("explicit Yes", denied["error"]["message"])

        status, _, _ = self.request("POST", "/api/decision", {"analysis_id": analysis_id, "choice": "yes"})
        self.assertEqual(status, 200)
        status, optimized, _ = self.request("POST", "/api/optimize", {"analysis_id": analysis_id})
        self.assertEqual(status, 201)
        self.assertIn("Python REST APIs", optimized["optimization"]["content"])
        self.assertNotIn("Kubernetes", optimized["optimization"]["content"])

        optimization_id = optimized["optimization"]["id"]
        status, download, headers = self.request("GET", f"/api/optimizations/{optimization_id}/download")
        self.assertEqual(status, 200)
        self.assertIn(b"Python REST APIs", download)
        self.assertTrue(any(name.lower() == "content-disposition" for name, _ in headers))

    def test_csrf_is_required_for_writes(self) -> None:
        self.initialize_session()
        self.csrf = "wrong"
        status, payload, _ = self.request("POST", "/api/job", {"text": SAMPLE_JOB})
        self.assertEqual(status, 403)
        self.assertEqual(payload["error"]["code"], "unauthorized")

    def test_security_headers_and_session_deletion(self) -> None:
        self.initialize_session()
        status, payload, headers = self.request("DELETE", "/api/session", {})
        self.assertEqual(status, 200)
        self.assertTrue(payload["deleted"])
        header_map = {name.lower(): value for name, value in headers}
        self.assertIn("frame-ancestors 'none'", header_map["content-security-policy"])
        self.assertEqual(header_map["x-content-type-options"], "nosniff")
        self.assertIn("Max-Age=0", header_map["set-cookie"])

    def test_rate_limiter_rejects_request_over_limit(self) -> None:
        limiter = RateLimiter()
        self.assertTrue(limiter.allow("127.0.0.1", "test", limit=2))
        self.assertTrue(limiter.allow("127.0.0.1", "test", limit=2))
        self.assertFalse(limiter.allow("127.0.0.1", "test", limit=2))


if __name__ == "__main__":
    unittest.main()
