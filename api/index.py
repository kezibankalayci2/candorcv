from __future__ import annotations

import json
import logging
import mimetypes
import os
import secrets
import time
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from app.config import load_settings
from app.errors import AppError, ValidationError
from app.stateless import StatelessService


MAX_REQUEST_BYTES = 4_400_000
LOGGER = logging.getLogger("candorcv_vercel")


def _service() -> StatelessService:
    settings = load_settings(Path.cwd())
    if os.getenv("VERCEL") and settings.app_secret in {"development-only-secret", "change-me-in-production"}:
        raise ValueError("APP_SECRET is required on Vercel")
    return StatelessService(settings)


SERVICE = _service()
STATIC_ROOT = Path.cwd() / "static"


class handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'; base-uri 'none'",
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Cache-Control": "no-store",
        }

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        for name, value in self._headers().items():
            self.send_header(name, value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", self.request_id)
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, path: str) -> bool:
        if path == "/":
            relative_path = "index.html"
        elif path == "/favicon.ico":
            relative_path = "assets/candorcv-logo-512.png"
        else:
            relative_path = path.lstrip("/")
        candidate = (STATIC_ROOT / relative_path).resolve()
        try:
            candidate.relative_to(STATIC_ROOT.resolve())
        except ValueError:
            return False
        if not candidate.is_file():
            return False

        body = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data: blob:; connect-src 'self'; base-uri 'none'; "
            "form-action 'self'; frame-ancestors 'none'",
        )
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cache-Control", "public, max-age=300")
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", self.request_id)
        self.end_headers()
        self.wfile.write(body)
        return True

    def _read_json(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValidationError("invalid_content_length", "The request length is invalid.") from exc
        if length <= 0 or length > MAX_REQUEST_BYTES:
            raise ValidationError("request_too_large", "The request body is empty or exceeds the Vercel limit.")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValidationError("invalid_json", "The request body is not valid JSON.") from exc
        if not isinstance(payload, dict):
            raise ValidationError("invalid_json_shape", "The request body must be a JSON object.")
        return payload

    def _handle(self, method: str) -> None:
        self.request_id = secrets.token_hex(8)
        started = time.perf_counter()
        path = urlparse(self.path).path
        status = 500
        try:
            if method == "GET" and self._send_static(path):
                status = 200
                return
            payload = self._read_json() if method in {"POST", "DELETE"} else None
            token = None
            if payload is not None:
                supplied = payload.pop("_session_state", None)
                token = supplied if isinstance(supplied, str) else None
            status, response = SERVICE.dispatch(
                method,
                path,
                payload,
                token=token or self.headers.get("X-Session-State"),
                csrf=self.headers.get("X-CSRF-Token"),
            )
            self._send_json(status, response)
        except AppError as exc:
            status = exc.status
            self._send_json(status, {"error": {"code": exc.code, "message": exc.message}})
        except Exception as exc:
            LOGGER.exception("request_failed", extra={"request_id": self.request_id, "error_type": type(exc).__name__})
            self._send_json(500, {"error": {"code": "internal_error", "message": "The request could not be completed safely."}})
        finally:
            LOGGER.info(
                "request_complete request_id=%s method=%s route=%s status=%s duration_ms=%s",
                self.request_id,
                method,
                path,
                status,
                round((time.perf_counter() - started) * 1000),
            )

    def do_GET(self) -> None:
        self._handle("GET")

    def do_POST(self) -> None:
        self._handle("POST")

    def do_DELETE(self) -> None:
        self._handle("DELETE")
