from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any

from .errors import ValidationError
from .language import is_probably_english


@dataclass(frozen=True)
class StructuredJob:
    title: str | None
    responsibilities: list[str]
    required: list[str]
    preferred: list[str]
    other: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


HEADING_KIND = {
    "responsibilities": "responsibilities",
    "what you will do": "responsibilities",
    "role responsibilities": "responsibilities",
    "requirements": "required",
    "required qualifications": "required",
    "minimum qualifications": "required",
    "must have": "required",
    "preferred qualifications": "preferred",
    "nice to have": "preferred",
    "preferred": "preferred",
}


def normalize_job(text: str, *, max_chars: int) -> StructuredJob:
    cleaned = text.replace("\x00", "").strip()
    if len(cleaned) < 100:
        raise ValidationError("job_too_short", "Please provide a complete English job description and requirements.")
    if len(cleaned) > max_chars:
        raise ValidationError("job_too_long", "The job description exceeds the allowed length.")
    if not is_probably_english(cleaned, minimum_words=20):
        raise ValidationError("job_not_english", "Please enter an English job description. The content is not translated automatically.")
    lines = [re.sub(r"^[\s\-•*\d.)]+", "", line).strip() for line in cleaned.splitlines()]
    lines = [line for line in lines if line]
    current = "other"
    buckets: dict[str, list[str]] = {"responsibilities": [], "required": [], "preferred": [], "other": []}
    title: str | None = None
    for index, line in enumerate(lines):
        normalized = re.sub(r"[:\s]+$", "", line.lower())
        if normalized in HEADING_KIND:
            current = HEADING_KIND[normalized]
            continue
        if index == 0 and len(line) <= 100 and not line.endswith("."):
            title = line
            continue
        buckets[current].append(line)
    if not buckets["required"]:
        requirement_markers = re.compile(r"\b(required|must|minimum|need|proficiency|experience with)\b", re.I)
        moved = [line for line in buckets["other"] if requirement_markers.search(line)]
        buckets["required"].extend(moved)
        buckets["other"] = [line for line in buckets["other"] if line not in moved]
    if not buckets["responsibilities"]:
        responsibility_markers = re.compile(r"\b(build|develop|design|lead|manage|deliver|maintain|collaborate)\b", re.I)
        moved = [line for line in buckets["other"] if responsibility_markers.search(line)]
        buckets["responsibilities"].extend(moved)
        buckets["other"] = [line for line in buckets["other"] if line not in moved]
    return StructuredJob(title, buckets["responsibilities"], buckets["required"], buckets["preferred"], buckets["other"])

