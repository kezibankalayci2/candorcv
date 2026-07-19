from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from typing import Any

from .ai import ANALYSIS_PROMPT_VERSION, provider_from_settings
from .analysis import SCORING_VERSION, analyze, validate_analysis
from .config import Settings
from .errors import AppError, ProviderError, UnauthorizedError, ValidationError
from .extractors import extract_cv
from .jobs import normalize_job
from .optimization import optimize_cv


MAX_STATE_BYTES = 1_500_000
MAX_EXTRACTED_TEXT_CHARS = 300_000


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


@dataclass(frozen=True)
class StateCodec:
    secret: str
    ttl_minutes: int

    def new(self) -> dict[str, Any]:
        now = int(time.time())
        return {
            "version": 1,
            "issued_at": now,
            "expires_at": now + self.ttl_minutes * 60,
            "nonce": secrets.token_urlsafe(18),
        }

    def encode(self, state: dict[str, Any]) -> str:
        raw = json.dumps(state, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
        if len(raw) > MAX_STATE_BYTES:
            raise ValidationError(
                "session_state_too_large",
                "This CV contains too much extracted text for the private browser session.",
            )
        body = _b64encode(raw)
        signature = hmac.new(self.secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
        return f"{body}.{_b64encode(signature)}"

    def decode(self, token: str) -> dict[str, Any]:
        try:
            body, supplied = token.split(".", 1)
            expected = hmac.new(self.secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
            if not hmac.compare_digest(expected, _b64decode(supplied)):
                raise ValueError("signature")
            state = json.loads(_b64decode(body).decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError, binascii.Error) as exc:
            raise UnauthorizedError("The private session state is invalid. Start a new session.") from exc
        if not isinstance(state, dict) or state.get("version") != 1:
            raise UnauthorizedError("The private session state is invalid. Start a new session.")
        if int(state.get("expires_at", 0)) <= int(time.time()):
            raise UnauthorizedError("The private session expired. Start a new session.")
        return state

    def csrf(self, state: dict[str, Any]) -> str:
        nonce = str(state.get("nonce", ""))
        return hmac.new(self.secret.encode("utf-8"), f"csrf:{nonce}".encode("utf-8"), hashlib.sha256).hexdigest()


class StatelessService:
    """Vercel-safe API service with signed, short-lived browser-held state."""

    def __init__(self, settings: Settings, *, secret: str | None = None) -> None:
        signing_secret = secret or settings.app_secret
        if len(signing_secret) < 32 or signing_secret in {"development-only-secret", "change-me-in-production"}:
            raise ValueError("APP_SECRET must be a unique value of at least 32 characters")
        self.settings = settings
        self.codec = StateCodec(signing_secret, settings.session_ttl_minutes)
        self.provider = provider_from_settings(settings)

    def _with_token(self, state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        return {**payload, "state_token": self.codec.encode(state)}

    def _require_state(self, token: str | None, csrf: str | None) -> dict[str, Any]:
        if not token:
            raise UnauthorizedError("Create a private session before sending data.")
        state = self.codec.decode(token)
        if not csrf or not hmac.compare_digest(self.codec.csrf(state), csrf):
            raise UnauthorizedError("The request verification token is missing or invalid.")
        return state

    def session(self, token: str | None) -> tuple[int, dict[str, Any]]:
        try:
            state = self.codec.decode(token) if token else self.codec.new()
        except UnauthorizedError:
            state = self.codec.new()
        cv = state.get("cv")
        job = state.get("job")
        analysis_record = state.get("analysis")
        summary = {
            "cv": {"id": cv["id"], "filename": cv["filename"]} if isinstance(cv, dict) else None,
            "job": {"id": job["id"]} if isinstance(job, dict) else None,
            "analysis": {"id": analysis_record["id"]} if isinstance(analysis_record, dict) else None,
        }
        return 200, self._with_token(
            state,
            {
                "csrf_token": self.codec.csrf(state),
                "expires_at": state["expires_at"],
                "state": summary,
                "storage_mode": "signed_browser_session",
                "ai_mode": "openai" if self.provider else "local",
                "model": self.settings.openai_model if self.provider else "local-source-preserving-v1",
            },
        )

    def dispatch(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None,
        *,
        token: str | None,
        csrf: str | None,
    ) -> tuple[int, dict[str, Any]]:
        if method == "GET" and path in {"/health", "/api/health"}:
            return 200, {"status": "ok", "version": "0.2.0", "runtime": "vercel-stateless"}
        if method == "GET" and path in {"/ready", "/api/ready"}:
            return 200, {"status": "ready", "storage": "signed_browser_session"}
        if method == "GET" and path == "/api/session":
            return self.session(token)
        if method not in {"POST", "DELETE"}:
            raise AppError("not_found", "The requested API endpoint was not found.", status=404)

        state = self._require_state(token, csrf)
        body = payload or {}
        if method == "DELETE" and path == "/api/session":
            fresh = self.codec.new()
            return 200, self._with_token(
                fresh,
                {"deleted": True, "csrf_token": self.codec.csrf(fresh)},
            )
        if method != "POST":
            raise AppError("not_found", "The requested API endpoint was not found.", status=404)

        if path == "/api/cv":
            return self._save_cv(state, body)
        if path == "/api/job":
            return self._save_job(state, body)
        if path == "/api/analyze":
            return self._analyze(state, body)
        if path == "/api/decision":
            return self._decision(state, body)
        if path == "/api/optimize":
            return self._optimize(state, body)
        raise AppError("not_found", "The requested API endpoint was not found.", status=404)

    def _save_cv(self, state: dict[str, Any], payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        filename = payload.get("filename")
        encoded = payload.get("data_base64")
        if not isinstance(filename, str) or not isinstance(encoded, str):
            raise ValidationError("invalid_cv_payload", "A filename and base64 file content are required.")
        try:
            data = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error) as exc:
            raise ValidationError("invalid_base64", "The CV content is not valid base64.") from exc
        cv = extract_cv(filename, data, max_bytes=min(self.settings.max_upload_bytes, 3_000_000))
        if len(cv.text) > MAX_EXTRACTED_TEXT_CHARS:
            raise ValidationError("cv_text_too_large", "The extracted CV text exceeds the safe session limit.")
        record = {
            "id": secrets.token_urlsafe(18),
            "filename": cv.filename,
            "content_hash": hashlib.sha256(data).hexdigest(),
            "extracted": cv.to_dict(),
        }
        state["cv"] = record
        state.pop("analysis", None)
        state.pop("decision", None)
        public = {"id": record["id"], "filename": record["filename"]}
        return 201, self._with_token(
            state,
            {
                "cv": public,
                "summary": {
                    "characters": len(cv.text),
                    "blocks": len(cv.blocks),
                    "sections": [key for key, value in cv.sections.items() if value],
                },
            },
        )

    def _save_job(self, state: dict[str, Any], payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        text = payload.get("text")
        if not isinstance(text, str):
            raise ValidationError("invalid_job_payload", "The job description text is required.")
        job = normalize_job(text, max_chars=self.settings.max_job_description_chars)
        record = {
            "id": secrets.token_urlsafe(18),
            "content_hash": hashlib.sha256(text.strip().encode("utf-8")).hexdigest(),
            "structured": job.to_dict(),
        }
        state["job"] = record
        state.pop("analysis", None)
        state.pop("decision", None)
        return 201, self._with_token(state, {"job": {"id": record["id"]}})

    def _analyze(self, state: dict[str, Any], payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        if not self.settings.analysis_enabled:
            raise AppError("analysis_disabled", "Analysis is temporarily unavailable.", status=503)
        cv = state.get("cv")
        job = state.get("job")
        if not isinstance(cv, dict) or not isinstance(job, dict):
            raise ValidationError("missing_inputs", "Upload a CV and add a job description first.")
        if payload.get("cv_id") != cv.get("id") or payload.get("job_id") != job.get("id"):
            raise UnauthorizedError("The CV and job identifiers do not belong to this private session.")
        result = analyze(cv["extracted"], job["structured"])
        model_version = "local-source-preserving-v1"
        if self.provider:
            try:
                result = self.provider.enhance_analysis(result)
                model_version = self.provider.model
            except ProviderError:
                result["mode"] = "local_fallback"
                result["provider_warning"] = "AI enhancement was unavailable. The verified local analysis is shown instead."
        validate_analysis(result, cv["extracted"])
        record = {
            "id": secrets.token_urlsafe(18),
            "cv_id": cv["id"],
            "job_id": job["id"],
            "result": result,
            "model_version": model_version,
            "prompt_version": ANALYSIS_PROMPT_VERSION,
            "scoring_version": SCORING_VERSION,
        }
        state["analysis"] = record
        state.pop("decision", None)
        return 201, self._with_token(state, {"analysis": {"id": record["id"], **result}})

    def _decision(self, state: dict[str, Any], payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        analysis_record = state.get("analysis")
        choice = payload.get("choice")
        if not isinstance(analysis_record, dict) or payload.get("analysis_id") != analysis_record.get("id"):
            raise UnauthorizedError("The analysis does not belong to this private session.")
        if choice not in {"yes", "no"}:
            raise ValidationError("invalid_decision", "Choose yes or no for the current analysis.")
        decision = {
            "id": secrets.token_urlsafe(18),
            "analysis_id": analysis_record["id"],
            "choice": choice,
            "decided_at": int(time.time()),
        }
        state["decision"] = decision
        return 200, self._with_token(state, {"decision": decision})

    def _optimize(self, state: dict[str, Any], payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        if not self.settings.optimization_enabled:
            raise AppError("optimization_disabled", "CV optimization is temporarily unavailable.", status=503)
        analysis_record = state.get("analysis")
        decision = state.get("decision")
        cv = state.get("cv")
        analysis_id = payload.get("analysis_id")
        if not isinstance(analysis_record, dict) or analysis_id != analysis_record.get("id"):
            raise UnauthorizedError("The analysis does not belong to this private session.")
        if not isinstance(decision, dict) or decision.get("analysis_id") != analysis_id or decision.get("choice") != "yes":
            raise UnauthorizedError("CV optimization requires an explicit Yes decision for this analysis.")
        if not isinstance(cv, dict) or analysis_record.get("cv_id") != cv.get("id"):
            raise UnauthorizedError("The source CV does not belong to this analysis.")
        content, references, model_version = optimize_cv(
            cv["extracted"], analysis_record["result"], self.provider
        )
        optimization = {
            "id": secrets.token_urlsafe(18),
            "analysis_id": analysis_id,
            "content": content,
            "references": references,
            "model_version": model_version,
        }
        return 201, self._with_token(state, {"optimization": optimization})
