from __future__ import annotations

import re
from collections import Counter
from typing import Any


SCORING_VERSION = "ats-match-v1"

STOPWORDS = {
    "about", "after", "also", "among", "and", "are", "based", "build", "building", "can", "company",
    "develop", "development", "experience", "for", "from", "have", "into", "job", "more", "our", "preferred",
    "required", "requirements", "responsibilities", "role", "skills", "team", "that", "the", "their", "this", "through",
    "using", "will", "with", "work", "working", "years", "you", "your",
}

KNOWN_TERMS = [
    "Python", "Java", "JavaScript", "TypeScript", "React", "Angular", "Vue", "Node.js", "C#", "C++", "Go", "Rust",
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "REST", "GraphQL", "Docker", "Kubernetes", "AWS", "Azure",
    "Google Cloud", "Git", "GitHub Actions", "CI/CD", "Terraform", "Linux", "Agile", "Scrum", "Machine Learning",
    "Data Analysis", "Power BI", "Tableau", "Excel", "FastAPI", "Django", "Flask", "Spring", ".NET", "HTML", "CSS",
]


def _canonical_text(text: str) -> str:
    return re.sub(r"[^a-z0-9+#./]+", " ", text.lower()).strip()


def _contains(text: str, term: str) -> bool:
    haystack = f" {_canonical_text(text)} "
    needle = _canonical_text(term)
    return bool(needle and f" {needle} " in haystack)


def extract_keywords(job_text: str, *, limit: int = 24) -> list[str]:
    found: list[str] = [term for term in KNOWN_TERMS if _contains(job_text, term)]
    words = re.findall(r"[A-Za-z][A-Za-z+#./-]{2,}", job_text)
    counts = Counter(word.lower() for word in words if word.lower() not in STOPWORDS)
    for word, count in counts.most_common(40):
        if count < 2:
            continue
        label = next((term for term in KNOWN_TERMS if term.lower() == word), word.title())
        if label not in found:
            found.append(label)
        if len(found) >= limit:
            break
    return found[:limit]


def _source_for(blocks: list[dict[str, Any]], term: str) -> dict[str, Any] | None:
    for block in blocks:
        if _contains(block["text"], term):
            return {
                "source_id": block["id"],
                "section": block["section"],
                "page": block.get("page"),
                "evidence": block["text"],
            }
    return None


def analyze(cv: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
    cv_text = cv["text"]
    job_text = "\n".join(
        filter(
            None,
            [job.get("title") or "", *job.get("required", []), *job.get("preferred", []), *job.get("responsibilities", []), *job.get("other", [])],
        )
    )
    keywords = extract_keywords(job_text)
    blocks = cv["blocks"]
    keyword_results: list[dict[str, Any]] = []
    supported: list[tuple[str, dict[str, Any]]] = []
    missing: list[str] = []
    for term in keywords:
        source = _source_for(blocks, term)
        if source:
            supported.append((term, source))
            keyword_results.append({"term": term, "status": "supported", "source": source})
        else:
            missing.append(term)
            keyword_results.append({"term": term, "status": "not_visible", "source": None})

    required_text = "\n".join(job.get("required", []))
    preferred_text = "\n".join(job.get("preferred", []))
    required_terms = [term for term in keywords if _contains(required_text, term)] or keywords[: min(8, len(keywords))]
    preferred_terms = [term for term in keywords if _contains(preferred_text, term)]
    required_supported = sum(1 for term in required_terms if _contains(cv_text, term))
    preferred_supported = sum(1 for term in preferred_terms if _contains(cv_text, term))
    required_score = required_supported / max(1, len(required_terms))
    preferred_score = preferred_supported / max(1, len(preferred_terms)) if preferred_terms else required_score
    overall_coverage = len(supported) / max(1, len(keywords))
    structure_sections = cv.get("sections", {})
    structure_hits = sum(1 for name in ("experience", "education", "skills") if structure_sections.get(name))
    structure_score = structure_hits / 3
    score = round(100 * (0.55 * required_score + 0.15 * preferred_score + 0.20 * overall_coverage + 0.10 * structure_score))
    score = max(0, min(100, score))

    strengths = [
        {
            "title": f"Evidence for {term}",
            "detail": f"The CV explicitly supports the job keyword “{term}”.",
            "source": source,
        }
        for term, source in supported[:6]
    ]
    missing_areas = [
        {
            "title": term,
            "detail": f"“{term}” appears important in the job description but is not visible in the CV. This does not mean the candidate lacks it.",
        }
        for term in missing[:8]
    ]
    improvements: list[str] = []
    if supported:
        improvements.append("Move the most relevant supported skills and experience closer to the top of the CV.")
    if missing:
        improvements.append("Review the not-visible requirements. Add them only if they are true and can be supported by the original CV content.")
    if structure_hits < 3:
        improvements.append("Use conventional ATS headings such as Experience, Education, and Skills where the source content supports them.")
    improvements.append("Keep formatting single-column, text-first, and free of tables or decorative graphics in the exported ATS version.")

    return {
        "score": score,
        "score_label": "Estimated match",
        "disclaimer": "This is an estimate, not a score from a specific ATS and not a hiring guarantee.",
        "dimensions": {
            "required_requirements": round(required_score * 100),
            "preferred_requirements": round(preferred_score * 100),
            "keyword_coverage": round(overall_coverage * 100),
            "ats_structure": round(structure_score * 100),
        },
        "strengths": strengths,
        "missing_areas": missing_areas,
        "keywords": keyword_results,
        "improvements": improvements,
        "mode": "local",
        "scoring_version": SCORING_VERSION,
    }


def validate_analysis(result: dict[str, Any], cv: dict[str, Any]) -> dict[str, Any]:
    score = result.get("score")
    if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100:
        raise ValueError("Analysis score must be an integer from 0 to 100")
    for field in ("strengths", "missing_areas", "keywords", "improvements"):
        if not isinstance(result.get(field), list):
            raise ValueError(f"Analysis field {field} must be a list")
    valid_sources = {block["id"] for block in cv["blocks"]}
    for strength in result["strengths"]:
        source = strength.get("source")
        if not source or source.get("source_id") not in valid_sources:
            raise ValueError("Every strength must have a valid CV source")
    return result

