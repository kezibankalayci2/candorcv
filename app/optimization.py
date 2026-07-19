from __future__ import annotations

import re
from typing import Any

from .ai import AIProvider
from .analysis import KNOWN_TERMS, _contains
from .errors import ValidationError


SECTION_ORDER = ["header", "summary", "skills", "experience", "projects", "education", "certifications"]
SECTION_LABELS = {
    "summary": "PROFESSIONAL SUMMARY",
    "skills": "SKILLS",
    "experience": "EXPERIENCE",
    "projects": "PROJECTS",
    "education": "EDUCATION",
    "certifications": "CERTIFICATIONS",
}


def _protected_tokens(text: str) -> set[str]:
    patterns = [
        r"\b\d+(?:[.,]\d+)?%?\b",
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        r"https?://\S+",
        r"\b(?:19|20)\d{2}\b",
    ]
    tokens: set[str] = set()
    for pattern in patterns:
        tokens.update(match.group(0) for match in re.finditer(pattern, text, re.I))
    return tokens


def _safe_rewrite(original: str, candidate: str, *, forbidden_keywords: list[str]) -> str:
    cleaned = re.sub(r"\s+", " ", candidate).strip()
    if not cleaned or len(cleaned) > max(500, len(original) * 3):
        return original
    if _protected_tokens(original) != _protected_tokens(cleaned):
        return original
    for keyword in forbidden_keywords:
        if _contains(cleaned, keyword) and not _contains(original, keyword):
            return original
    for term in KNOWN_TERMS:
        if _contains(cleaned, term) and not _contains(original, term):
            return original
    return cleaned


def optimize_cv(
    cv: dict[str, Any],
    analysis: dict[str, Any],
    provider: AIProvider | None,
) -> tuple[str, list[dict[str, Any]], str]:
    blocks = cv["blocks"]
    supported_keywords = [item["term"] for item in analysis.get("keywords", []) if item.get("status") == "supported"]
    forbidden_keywords = [item["term"] for item in analysis.get("keywords", []) if item.get("status") != "supported"]
    rewrites: dict[str, str] = {}
    model_version = "local-source-preserving-v1"
    if provider:
        rewrites = provider.rewrite_blocks(
            blocks,
            supported_keywords=supported_keywords,
            forbidden_keywords=forbidden_keywords,
        )
        model_version = provider.model
    valid_ids = {block["id"] for block in blocks}
    if any(source_id not in valid_ids for source_id in rewrites):
        raise ValidationError("invalid_source_reference", "The generated CV contained an unknown source reference.")

    ordered_sections = SECTION_ORDER + sorted({block["section"] for block in blocks} - set(SECTION_ORDER))
    output_lines: list[str] = []
    references: list[dict[str, Any]] = []
    for section in ordered_sections:
        section_blocks = [block for block in blocks if block["section"] == section]
        if not section_blocks:
            continue
        if section != "header":
            output_lines.extend(["", SECTION_LABELS.get(section, section.upper()), ""])
        for block in section_blocks:
            original = block["text"]
            candidate = rewrites.get(block["id"], original)
            optimized = _safe_rewrite(original, candidate, forbidden_keywords=forbidden_keywords)
            prefix = "" if section in {"header", "summary"} else "• "
            output_lines.append(prefix + optimized)
            references.append(
                {
                    "source_id": block["id"],
                    "section": section,
                    "page": block.get("page"),
                    "original": original,
                    "optimized": optimized,
                    "changed": optimized != original,
                }
            )
    content = "\n".join(output_lines).strip() + "\n"
    if not content.strip() or len(references) != len(blocks):
        raise ValidationError("optimization_incomplete", "The CV could not be reconstructed without losing source content.")
    return content, references, model_version

