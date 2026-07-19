from __future__ import annotations

import json
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

from .errors import NotFoundError, UnauthorizedError


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: datetime) -> str:
    return value.isoformat(timespec="seconds")


class Repository:
    def __init__(self, path: Path, session_ttl_minutes: int) -> None:
        self.path = path
        self.session_ttl_minutes = session_ttl_minutes
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connection() as db:
            db.executescript(
                """
                PRAGMA journal_mode = WAL;
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    csrf_token TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS cvs (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                    version INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    media_type TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    extracted_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(session_id, version)
                );
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                    version INTEGER NOT NULL,
                    content_hash TEXT NOT NULL,
                    raw_text TEXT NOT NULL,
                    structured_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(session_id, version)
                );
                CREATE TABLE IF NOT EXISTS analyses (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                    cv_id TEXT NOT NULL REFERENCES cvs(id) ON DELETE CASCADE,
                    job_id TEXT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
                    result_json TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    scoring_version TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS decisions (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                    analysis_id TEXT NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
                    choice TEXT NOT NULL CHECK(choice IN ('yes', 'no')),
                    created_at TEXT NOT NULL,
                    UNIQUE(session_id, analysis_id)
                );
                CREATE TABLE IF NOT EXISTS optimizations (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                    analysis_id TEXT NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
                    decision_id TEXT NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    references_json TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(session_id, analysis_id)
                );
                CREATE INDEX IF NOT EXISTS idx_cvs_session ON cvs(session_id, created_at);
                CREATE INDEX IF NOT EXISTS idx_jobs_session ON jobs(session_id, created_at);
                CREATE INDEX IF NOT EXISTS idx_analyses_session ON analyses(session_id, created_at);
                """
            )

    def ping(self) -> bool:
        with self.connection() as db:
            return db.execute("SELECT 1").fetchone()[0] == 1

    def create_session(self) -> dict[str, str]:
        session_id = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        now = utc_now()
        expires = now + timedelta(minutes=self.session_ttl_minutes)
        with self.connection() as db:
            db.execute(
                "INSERT INTO sessions(id, csrf_token, created_at, expires_at) VALUES (?, ?, ?, ?)",
                (session_id, csrf, iso(now), iso(expires)),
            )
        return {"id": session_id, "csrf_token": csrf, "expires_at": iso(expires)}

    def require_session(self, session_id: str | None) -> sqlite3.Row:
        if not session_id:
            raise UnauthorizedError("A valid session is required.")
        expired = False
        with self.connection() as db:
            row = db.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if not row:
                raise UnauthorizedError("The session is missing or has expired.")
            if datetime.fromisoformat(row["expires_at"]) <= utc_now():
                db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
                expired = True
            else:
                expires = utc_now() + timedelta(minutes=self.session_ttl_minutes)
                db.execute("UPDATE sessions SET expires_at = ? WHERE id = ?", (iso(expires), session_id))
        if expired:
            raise UnauthorizedError("The session has expired.")
        assert row is not None
        return row

    def validate_csrf(self, session_id: str, token: str | None) -> None:
        row = self.require_session(session_id)
        if not token or not secrets.compare_digest(row["csrf_token"], token):
            raise UnauthorizedError("The request verification token is invalid.")

    def cleanup_expired(self) -> int:
        with self.connection() as db:
            cursor = db.execute("DELETE FROM sessions WHERE expires_at <= ?", (iso(utc_now()),))
            return cursor.rowcount

    def delete_session(self, session_id: str) -> None:
        with self.connection() as db:
            db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    def save_cv(self, session_id: str, *, filename: str, media_type: str, content_hash: str, extracted: dict[str, Any]) -> dict[str, Any]:
        self.require_session(session_id)
        with self.connection() as db:
            version = db.execute("SELECT COALESCE(MAX(version), 0) + 1 FROM cvs WHERE session_id = ?", (session_id,)).fetchone()[0]
            cv_id = secrets.token_urlsafe(18)
            created = iso(utc_now())
            db.execute(
                "INSERT INTO cvs VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (cv_id, session_id, version, filename, media_type, content_hash, json.dumps(extracted), created),
            )
        return {"id": cv_id, "version": version, "filename": filename, "media_type": media_type, "created_at": created}

    def save_job(self, session_id: str, *, content_hash: str, raw_text: str, structured: dict[str, Any]) -> dict[str, Any]:
        self.require_session(session_id)
        with self.connection() as db:
            version = db.execute("SELECT COALESCE(MAX(version), 0) + 1 FROM jobs WHERE session_id = ?", (session_id,)).fetchone()[0]
            job_id = secrets.token_urlsafe(18)
            created = iso(utc_now())
            db.execute(
                "INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)",
                (job_id, session_id, version, content_hash, raw_text, json.dumps(structured), created),
            )
        return {"id": job_id, "version": version, "created_at": created, "structured": structured}

    def _owned_row(self, table: str, record_id: str, session_id: str) -> sqlite3.Row:
        if table not in {"cvs", "jobs", "analyses", "decisions", "optimizations"}:
            raise ValueError("Unsupported table")
        self.require_session(session_id)
        with self.connection() as db:
            row = db.execute(f"SELECT * FROM {table} WHERE id = ? AND session_id = ?", (record_id, session_id)).fetchone()
        if not row:
            raise NotFoundError()
        return row

    def get_cv(self, record_id: str, session_id: str) -> dict[str, Any]:
        row = self._owned_row("cvs", record_id, session_id)
        return {**dict(row), "extracted": json.loads(row["extracted_json"])}

    def get_job(self, record_id: str, session_id: str) -> dict[str, Any]:
        row = self._owned_row("jobs", record_id, session_id)
        return {**dict(row), "structured": json.loads(row["structured_json"])}

    def save_analysis(
        self,
        session_id: str,
        *,
        cv_id: str,
        job_id: str,
        result: dict[str, Any],
        model_version: str,
        prompt_version: str,
        scoring_version: str,
    ) -> dict[str, Any]:
        self.get_cv(cv_id, session_id)
        self.get_job(job_id, session_id)
        analysis_id = secrets.token_urlsafe(18)
        created = iso(utc_now())
        with self.connection() as db:
            db.execute(
                "INSERT INTO analyses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (analysis_id, session_id, cv_id, job_id, json.dumps(result), model_version, prompt_version, scoring_version, created),
            )
        return {"id": analysis_id, "created_at": created, **result}

    def get_analysis(self, record_id: str, session_id: str) -> dict[str, Any]:
        row = self._owned_row("analyses", record_id, session_id)
        return {**dict(row), "result": json.loads(row["result_json"])}

    def save_decision(self, session_id: str, *, analysis_id: str, choice: str) -> dict[str, Any]:
        if choice not in {"yes", "no"}:
            raise ValueError("Decision must be yes or no")
        self.get_analysis(analysis_id, session_id)
        decision_id = secrets.token_urlsafe(18)
        created = iso(utc_now())
        with self.connection() as db:
            existing = db.execute(
                "SELECT id FROM decisions WHERE session_id = ? AND analysis_id = ?", (session_id, analysis_id)
            ).fetchone()
            if existing:
                db.execute(
                    "UPDATE decisions SET choice = ?, created_at = ? WHERE id = ?",
                    (choice, created, existing["id"]),
                )
                decision_id = existing["id"]
            else:
                db.execute(
                    "INSERT INTO decisions VALUES (?, ?, ?, ?, ?)",
                    (decision_id, session_id, analysis_id, choice, created),
                )
        return {"id": decision_id, "analysis_id": analysis_id, "choice": choice, "created_at": created}

    def get_decision_for_analysis(self, analysis_id: str, session_id: str) -> dict[str, Any] | None:
        self.get_analysis(analysis_id, session_id)
        with self.connection() as db:
            row = db.execute(
                "SELECT * FROM decisions WHERE analysis_id = ? AND session_id = ?", (analysis_id, session_id)
            ).fetchone()
        return dict(row) if row else None

    def save_optimization(
        self,
        session_id: str,
        *,
        analysis_id: str,
        decision_id: str,
        content: str,
        references: list[dict[str, Any]],
        model_version: str,
    ) -> dict[str, Any]:
        optimization_id = secrets.token_urlsafe(18)
        created = iso(utc_now())
        with self.connection() as db:
            existing = db.execute(
                "SELECT id FROM optimizations WHERE session_id = ? AND analysis_id = ?", (session_id, analysis_id)
            ).fetchone()
            if existing:
                db.execute(
                    "UPDATE optimizations SET decision_id = ?, content = ?, references_json = ?, model_version = ?, created_at = ? WHERE id = ?",
                    (decision_id, content, json.dumps(references), model_version, created, existing["id"]),
                )
                optimization_id = existing["id"]
            else:
                db.execute(
                    "INSERT INTO optimizations VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (optimization_id, session_id, analysis_id, decision_id, content, json.dumps(references), model_version, created),
                )
        return {"id": optimization_id, "analysis_id": analysis_id, "content": content, "references": references, "created_at": created}

    def get_optimization(self, record_id: str, session_id: str) -> dict[str, Any]:
        row = self._owned_row("optimizations", record_id, session_id)
        return {**dict(row), "references": json.loads(row["references_json"])}

    def session_summary(self, session_id: str) -> dict[str, Any]:
        row = self.require_session(session_id)
        with self.connection() as db:
            cv = db.execute("SELECT id, version, filename FROM cvs WHERE session_id = ? ORDER BY version DESC LIMIT 1", (session_id,)).fetchone()
            job = db.execute("SELECT id, version FROM jobs WHERE session_id = ? ORDER BY version DESC LIMIT 1", (session_id,)).fetchone()
            analysis = db.execute("SELECT id FROM analyses WHERE session_id = ? ORDER BY created_at DESC LIMIT 1", (session_id,)).fetchone()
        return {
            "expires_at": row["expires_at"],
            "cv": dict(cv) if cv else None,
            "job": dict(job) if job else None,
            "analysis": dict(analysis) if analysis else None,
        }
