from __future__ import annotations

import base64
import binascii
import hashlib
import json
import logging
import mimetypes
import re
import secrets
import sys
import threading
import time
from collections import defaultdict, deque
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .ai import ANALYSIS_PROMPT_VERSION, provider_from_settings
from .analysis import SCORING_VERSION, analyze, validate_analysis
from .config import Settings, load_settings
from .errors import AppError, ProviderError, UnauthorizedError, ValidationError
from .extractors import extract_cv
from .jobs import normalize_job
from .optimization import optimize_cv
from .repository import Repository


LOGGER = logging.getLogger("candorcv")
SESSION_COOKIE = "candorcv_session"
MAX_JSON_OVERHEAD = 2 * 1024 * 1024
REQUEST_TIMEOUT_SECONDS = 30


class RateLimiter:
    """Small in-process abuse guard; deployment proxies should add a shared limit too."""

    def __init__(self) -> None:
        self._events: dict[tuple[str, str], deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, client: str, bucket: str, *, limit: int, window_seconds: int = 60) -> bool:
        now = time.monotonic()
        key = (client, bucket)
        with self._lock:
            events = self._events[key]
            cutoff = now - window_seconds
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= limit:
                return False
            events.append(now)
            return True


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    LOGGER.handlers[:] = [handler]
    LOGGER.setLevel(logging.INFO)


def log_event(event: str, **fields: Any) -> None:
    safe = {"event": event, **fields}
    LOGGER.info(json.dumps(safe, separators=(",", ":"), default=str))


class AppServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], settings: Settings) -> None:
        self.settings = settings
        self.repository = Repository(settings.database_path, settings.session_ttl_minutes)
        self.provider = provider_from_settings(settings)
        self.rate_limiter = RateLimiter()
        self.static_root = Path(__file__).resolve().parent.parent / "static"
        super().__init__(address, AppHandler)


class AppHandler(BaseHTTPRequestHandler):
    server: AppServer
    protocol_version = "HTTP/1.1"

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(REQUEST_TIMEOUT_SECONDS)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _correlation_id(self) -> str:
        value = self.headers.get("X-Request-ID", "")
        return value[:64] if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", value) else secrets.token_hex(8)

    def _security_headers(self) -> dict[str, str]:
        headers = {
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'",
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cache-Control": "no-store",
        }
        if self.server.settings.production:
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return headers

    def _send_bytes(
        self,
        status: int,
        body: bytes,
        content_type: str,
        *,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        for key, value in self._security_headers().items():
            self.send_header(key, value)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", getattr(self, "request_id", "unknown"))
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_json(
        self,
        status: int,
        payload: dict[str, Any],
        *,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8", extra_headers=extra_headers)

    def _cookies(self) -> SimpleCookie[str]:
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get("Cookie", ""))
        except Exception:
            pass
        return cookie

    def _session_id(self) -> str | None:
        morsel = self._cookies().get(SESSION_COOKIE)
        return morsel.value if morsel else None

    def _session_cookie(self, session_id: str, *, delete: bool = False) -> str:
        parts = [f"{SESSION_COOKIE}={'' if delete else session_id}", "Path=/", "HttpOnly", "SameSite=Strict"]
        if self.server.settings.production:
            parts.append("Secure")
        if delete:
            parts.extend(["Max-Age=0", "Expires=Thu, 01 Jan 1970 00:00:00 GMT"])
        else:
            parts.append(f"Max-Age={self.server.settings.session_ttl_minutes * 60}")
        return "; ".join(parts)

    def _require_write_session(self) -> str:
        session_id = self._session_id()
        if not session_id:
            raise UnauthorizedError("Create a session before sending data.")
        self.server.repository.validate_csrf(session_id, self.headers.get("X-CSRF-Token"))
        return session_id

    def _read_json(self) -> dict[str, Any]:
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].lower()
        if content_type != "application/json":
            raise ValidationError("unsupported_content_type", "Requests must use application/json.")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValidationError("invalid_content_length", "The request length is invalid.") from exc
        maximum = int(self.server.settings.max_upload_bytes * 1.5) + MAX_JSON_OVERHEAD
        if length <= 0 or length > maximum:
            raise ValidationError("request_too_large", "The request body is empty or exceeds the safe limit.")
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValidationError("invalid_json", "The request body is not valid JSON.") from exc
        if not isinstance(payload, dict):
            raise ValidationError("invalid_json_shape", "The request body must be a JSON object.")
        return payload

    def _route(self) -> tuple[str, str]:
        parsed = urlparse(self.path)
        return parsed.path, parsed.query

    def _handle(self) -> None:
        self.request_id = self._correlation_id()
        start = time.perf_counter()
        status = 500
        path, _ = self._route()
        try:
            bucket = "expensive" if path in {"/api/analyze", "/api/optimize"} else "default"
            limit = 20 if bucket == "expensive" else 120
            if not self.server.rate_limiter.allow(self.client_address[0], bucket, limit=limit):
                raise AppError("rate_limited", "Too many requests. Wait briefly and try again.", status=429)
            if self.command == "GET":
                status = self._get(path)
            elif self.command == "POST":
                status = self._post(path)
            elif self.command == "DELETE":
                status = self._delete(path)
            elif self.command == "HEAD":
                status = self._get(path)
            else:
                self._send_json(405, {"error": {"code": "method_not_allowed", "message": "Method not allowed."}})
                status = 405
        except AppError as exc:
            status = exc.status
            self._send_json(exc.status, {"error": {"code": exc.code, "message": exc.message}})
        except Exception as exc:
            status = 500
            log_event("unhandled_error", request_id=self.request_id, error_type=type(exc).__name__)
            self._send_json(500, {"error": {"code": "internal_error", "message": "The request could not be completed safely."}})
        finally:
            log_event(
                "request_complete",
                request_id=self.request_id,
                method=self.command,
                route=path,
                status=status,
                duration_ms=round((time.perf_counter() - start) * 1000),
            )

    def do_GET(self) -> None:
        self._handle()

    def do_HEAD(self) -> None:
        self._handle()

    def do_POST(self) -> None:
        self._handle()

    def do_DELETE(self) -> None:
        self._handle()

    def _get(self, path: str) -> int:
        if path == "/health":
            self._send_json(200, {"status": "ok", "version": "0.1.0"})
            return 200
        if path == "/ready":
            ready = self.server.repository.ping()
            self._send_json(200 if ready else 503, {"status": "ready" if ready else "not_ready"})
            return 200 if ready else 503
        if path == "/api/session":
            self.server.repository.cleanup_expired()
            session_id = self._session_id()
            headers: dict[str, str] = {}
            try:
                if session_id:
                    row = self.server.repository.require_session(session_id)
                    csrf = row["csrf_token"]
                else:
                    raise UnauthorizedError()
            except UnauthorizedError:
                created = self.server.repository.create_session()
                session_id = created["id"]
                csrf = created["csrf_token"]
                headers["Set-Cookie"] = self._session_cookie(session_id)
            summary = self.server.repository.session_summary(session_id)
            self._send_json(
                200,
                {
                    "csrf_token": csrf,
                    "expires_at": summary["expires_at"],
                    "state": {"cv": summary["cv"], "job": summary["job"], "analysis": summary["analysis"]},
                    "ai_mode": "openai" if self.server.provider else "local",
                    "model": self.server.settings.openai_model if self.server.provider else "local-source-preserving-v1",
                },
                extra_headers=headers,
            )
            return 200
        download = re.fullmatch(r"/api/optimizations/([A-Za-z0-9_-]+)/download", path)
        if download:
            session_id = self._session_id()
            if not session_id:
                raise UnauthorizedError()
            record = self.server.repository.get_optimization(download.group(1), session_id)
            headers = {"Content-Disposition": 'attachment; filename="optimized-cv.txt"'}
            self._send_bytes(200, record["content"].encode("utf-8"), "text/plain; charset=utf-8", extra_headers=headers)
            return 200
        return self._serve_static(path)

    def _serve_static(self, path: str) -> int:
        relative = "index.html" if path in {"", "/"} else path.lstrip("/")
        requested = (self.server.static_root / relative).resolve()
        try:
            requested.relative_to(self.server.static_root.resolve())
        except ValueError:
            raise ValidationError("invalid_path", "The requested path is invalid.")
        if not requested.is_file():
            requested = self.server.static_root / "index.html"
        content_type = mimetypes.guess_type(requested.name)[0] or "application/octet-stream"
        cache = "public, max-age=3600" if requested.name != "index.html" else "no-store"
        self._send_bytes(200, requested.read_bytes(), content_type, extra_headers={"Cache-Control": cache})
        return 200

    def _post(self, path: str) -> int:
        session_id = self._require_write_session()
        payload = self._read_json()
        if path == "/api/cv":
            filename = payload.get("filename")
            encoded = payload.get("data_base64")
            if not isinstance(filename, str) or not isinstance(encoded, str):
                raise ValidationError("invalid_cv_payload", "A filename and base64 file content are required.")
            try:
                data = base64.b64decode(encoded, validate=True)
            except (ValueError, binascii.Error) as exc:
                raise ValidationError("invalid_base64", "The CV content is not valid base64.") from exc
            cv = extract_cv(filename, data, max_bytes=self.server.settings.max_upload_bytes)
            saved = self.server.repository.save_cv(
                session_id,
                filename=cv.filename,
                media_type=cv.media_type,
                content_hash=hashlib.sha256(data).hexdigest(),
                extracted=cv.to_dict(),
            )
            self._send_json(201, {"cv": saved, "summary": {"characters": len(cv.text), "blocks": len(cv.blocks), "sections": [key for key, value in cv.sections.items() if value]}})
            return 201
        if path == "/api/job":
            text = payload.get("text")
            if not isinstance(text, str):
                raise ValidationError("invalid_job_payload", "The job description text is required.")
            job = normalize_job(text, max_chars=self.server.settings.max_job_description_chars)
            saved = self.server.repository.save_job(
                session_id,
                content_hash=hashlib.sha256(text.strip().encode("utf-8")).hexdigest(),
                raw_text=text.strip(),
                structured=job.to_dict(),
            )
            self._send_json(201, {"job": saved})
            return 201
        if path == "/api/analyze":
            if not self.server.settings.analysis_enabled:
                raise AppError("analysis_disabled", "Analysis is temporarily unavailable.", status=503)
            cv_id, job_id = payload.get("cv_id"), payload.get("job_id")
            if not isinstance(cv_id, str) or not isinstance(job_id, str):
                raise ValidationError("invalid_analysis_payload", "CV and job identifiers are required.")
            cv_record = self.server.repository.get_cv(cv_id, session_id)
            job_record = self.server.repository.get_job(job_id, session_id)
            result = analyze(cv_record["extracted"], job_record["structured"])
            model_version = "local-source-preserving-v1"
            if self.server.provider:
                try:
                    result = self.server.provider.enhance_analysis(result)
                    model_version = self.server.provider.model
                except ProviderError:
                    result["mode"] = "local_fallback"
                    result["provider_warning"] = "AI enhancement was unavailable. The verified local analysis is shown instead."
            validate_analysis(result, cv_record["extracted"])
            saved = self.server.repository.save_analysis(
                session_id,
                cv_id=cv_id,
                job_id=job_id,
                result=result,
                model_version=model_version,
                prompt_version=ANALYSIS_PROMPT_VERSION,
                scoring_version=SCORING_VERSION,
            )
            self._send_json(201, {"analysis": saved})
            return 201
        if path == "/api/decision":
            analysis_id, choice = payload.get("analysis_id"), payload.get("choice")
            if not isinstance(analysis_id, str) or choice not in {"yes", "no"}:
                raise ValidationError("invalid_decision", "Choose yes or no for the current analysis.")
            decision = self.server.repository.save_decision(session_id, analysis_id=analysis_id, choice=choice)
            self._send_json(200, {"decision": decision})
            return 200
        if path == "/api/optimize":
            if not self.server.settings.optimization_enabled:
                raise AppError("optimization_disabled", "CV optimization is temporarily unavailable.", status=503)
            analysis_id = payload.get("analysis_id")
            if not isinstance(analysis_id, str):
                raise ValidationError("invalid_optimization_payload", "The analysis identifier is required.")
            analysis_record = self.server.repository.get_analysis(analysis_id, session_id)
            decision = self.server.repository.get_decision_for_analysis(analysis_id, session_id)
            if not decision or decision["choice"] != "yes":
                raise UnauthorizedError("CV optimization requires an explicit Yes decision for this analysis.")
            cv_record = self.server.repository.get_cv(analysis_record["cv_id"], session_id)
            content, references, model_version = optimize_cv(
                cv_record["extracted"], analysis_record["result"], self.server.provider
            )
            saved = self.server.repository.save_optimization(
                session_id,
                analysis_id=analysis_id,
                decision_id=decision["id"],
                content=content,
                references=references,
                model_version=model_version,
            )
            self._send_json(201, {"optimization": saved})
            return 201
        raise AppError("not_found", "The requested API endpoint was not found.", status=404)

    def _delete(self, path: str) -> int:
        if path != "/api/session":
            raise AppError("not_found", "The requested API endpoint was not found.", status=404)
        session_id = self._require_write_session()
        self.server.repository.delete_session(session_id)
        self._send_json(200, {"deleted": True}, extra_headers={"Set-Cookie": self._session_cookie("", delete=True)})
        return 200


def main() -> None:
    configure_logging()
    settings = load_settings()
    server = AppServer((settings.host, settings.port), settings)
    server.repository.cleanup_expired()
    log_event(
        "server_start",
        host=settings.host,
        port=settings.port,
        environment=settings.environment,
        ai_mode="openai" if server.provider else "local",
    )
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        log_event("server_stop")


if __name__ == "__main__":
    main()
