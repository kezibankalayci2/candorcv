from __future__ import annotations

import base64
import tempfile
import unittest
from pathlib import Path

from app.config import Settings
from app.errors import UnauthorizedError
from app.stateless import StateCodec, StatelessService
from tests.helpers import SAMPLE_CV_PARAGRAPHS, SAMPLE_JOB, make_docx


class StatelessServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        settings = Settings(
            host="127.0.0.1",
            port=8000,
            environment="test",
            app_secret="a" * 32,
            database_path=Path(self.temp.name) / "unused.db",
            session_ttl_minutes=60,
            max_upload_bytes=3_000_000,
            max_job_description_chars=30_000,
            openai_api_key=None,
            openai_api_base="https://api.openai.com/v1",
            openai_model="gpt-5.6-luna",
            openai_timeout_seconds=5,
        )
        self.service = StatelessService(settings)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_signed_state_rejects_tampering(self) -> None:
        codec = StateCodec("b" * 32, 60)
        token = codec.encode(codec.new())
        changed = ("A" if token[0] != "A" else "B") + token[1:]
        with self.assertRaises(UnauthorizedError):
            codec.decode(changed)

    def test_full_stateless_flow_requires_yes(self) -> None:
        _, session = self.service.session(None)
        token, csrf = session["state_token"], session["csrf_token"]
        cv_data = base64.b64encode(make_docx(SAMPLE_CV_PARAGRAPHS)).decode("ascii")
        _, cv_response = self.service.dispatch(
            "POST", "/api/cv", {"filename": "resume.docx", "data_base64": cv_data}, token=token, csrf=csrf
        )
        token = cv_response["state_token"]
        _, job_response = self.service.dispatch(
            "POST", "/api/job", {"text": SAMPLE_JOB}, token=token, csrf=csrf
        )
        token = job_response["state_token"]
        _, analysis_response = self.service.dispatch(
            "POST",
            "/api/analyze",
            {"cv_id": cv_response["cv"]["id"], "job_id": job_response["job"]["id"]},
            token=token,
            csrf=csrf,
        )
        token = analysis_response["state_token"]
        analysis_id = analysis_response["analysis"]["id"]
        with self.assertRaises(UnauthorizedError):
            self.service.dispatch(
                "POST", "/api/optimize", {"analysis_id": analysis_id}, token=token, csrf=csrf
            )
        _, decision_response = self.service.dispatch(
            "POST",
            "/api/decision",
            {"analysis_id": analysis_id, "choice": "yes"},
            token=token,
            csrf=csrf,
        )
        _, optimized = self.service.dispatch(
            "POST",
            "/api/optimize",
            {"analysis_id": analysis_id},
            token=decision_response["state_token"],
            csrf=csrf,
        )
        self.assertIn("Python REST APIs", optimized["optimization"]["content"])
        self.assertNotIn("Kubernetes", optimized["optimization"]["content"])


if __name__ == "__main__":
    unittest.main()
