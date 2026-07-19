from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _int_env(name: str, default: int, *, minimum: int, maximum: int) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name, "true" if default else "false").strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be true or false")


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    environment: str
    app_secret: str
    database_path: Path
    session_ttl_minutes: int
    max_upload_bytes: int
    max_job_description_chars: int
    openai_api_key: str | None
    openai_api_base: str
    openai_model: str
    openai_timeout_seconds: int
    analysis_enabled: bool = True
    optimization_enabled: bool = True

    @property
    def production(self) -> bool:
        return self.environment.lower() == "production"


def load_settings(root: Path | None = None) -> Settings:
    project_root = root or Path.cwd()
    _load_dotenv(project_root / ".env")
    environment = os.getenv("APP_ENV", "development")
    secret = os.getenv("APP_SECRET", "development-only-secret")
    if environment.lower() == "production" and (
        len(secret) < 32 or secret in {"change-me-in-production", "development-only-secret"}
    ):
        raise ValueError("APP_SECRET must be a unique value of at least 32 characters in production")
    database_raw = os.getenv("DATABASE_PATH", ".data/app.db")
    database_path = Path(database_raw)
    if not database_path.is_absolute():
        database_path = project_root / database_path
    return Settings(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=_int_env("APP_PORT", 8000, minimum=1, maximum=65535),
        environment=environment,
        app_secret=secret,
        database_path=database_path,
        session_ttl_minutes=_int_env("SESSION_TTL_MINUTES", 120, minimum=5, maximum=1440),
        max_upload_bytes=_int_env("MAX_UPLOAD_BYTES", 3_000_000, minimum=1024, maximum=20_971_520),
        max_job_description_chars=_int_env(
            "MAX_JOB_DESCRIPTION_CHARS", 30_000, minimum=1_000, maximum=100_000
        ),
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1").rstrip("/"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
        openai_timeout_seconds=_int_env("OPENAI_TIMEOUT_SECONDS", 60, minimum=5, maximum=300),
        analysis_enabled=_bool_env("ANALYSIS_ENABLED", True),
        optimization_enabled=_bool_env("OPTIMIZATION_ENABLED", True),
    )
