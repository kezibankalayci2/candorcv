from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol

from .config import Settings
from .errors import ProviderError


LOGGER = logging.getLogger("candorcv.ai")
ANALYSIS_PROMPT_VERSION = "analysis-grounding-v1"
OPTIMIZATION_PROMPT_VERSION = "optimization-grounding-v1"


class AIProvider(Protocol):
    model: str

    def enhance_analysis(self, result: dict[str, Any]) -> dict[str, Any]: ...

    def rewrite_blocks(
        self,
        blocks: list[dict[str, Any]],
        *,
        supported_keywords: list[str],
        forbidden_keywords: list[str],
    ) -> dict[str, str]: ...


@dataclass
class OpenAIProvider:
    api_key: str
    api_base: str
    model: str
    timeout_seconds: int

    def _complete_json(self, system: str, user_payload: dict[str, Any]) -> dict[str, Any]:
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
            ],
            "response_format": {"type": "json_object"},
        }
        request = urllib.request.Request(
            f"{self.api_base}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "candorcv/0.2.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
            content = payload["choices"][0]["message"]["content"]
            result = json.loads(content)
            if not isinstance(result, dict):
                raise ValueError("Expected an object")
            return result
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, KeyError, IndexError, json.JSONDecodeError, ValueError) as exc:
            LOGGER.warning("openai_request_failed", extra={"event": "openai_request_failed", "error_type": type(exc).__name__})
            raise ProviderError() from exc

    def enhance_analysis(self, result: dict[str, Any]) -> dict[str, Any]:
        system = (
            "You improve the clarity of an ATS CV analysis. The supplied JSON is the complete evidence boundary. "
            "Do not add candidate facts, skills, experience, education, certifications, achievements, dates, metrics, or keywords. "
            "Return JSON with exactly: summary (string) and improvements (array of 2-5 concise strings). "
            "State that the score is estimated. Missing means not visible in the CV, not that the candidate lacks the skill."
        )
        payload = self._complete_json(system, {"prompt_version": ANALYSIS_PROMPT_VERSION, "analysis": result})
        summary = payload.get("summary")
        improvements = payload.get("improvements")
        enhanced = dict(result)
        if isinstance(summary, str) and 20 <= len(summary) <= 600:
            enhanced["summary"] = summary.strip()
        if isinstance(improvements, list) and 2 <= len(improvements) <= 5 and all(isinstance(item, str) and 10 <= len(item) <= 300 for item in improvements):
            enhanced["improvements"] = [item.strip() for item in improvements]
        enhanced["mode"] = "ai"
        enhanced["model_version"] = self.model
        return enhanced

    def rewrite_blocks(
        self,
        blocks: list[dict[str, Any]],
        *,
        supported_keywords: list[str],
        forbidden_keywords: list[str],
    ) -> dict[str, str]:
        system = (
            "You edit an English CV for clarity and ATS readability. Each block is source evidence. "
            "Rewrite only the wording of that exact block. Never add or infer experience, skills, tools, education, certifications, "
            "responsibilities, dates, metrics, achievements, employers, job titles, or seniority. Preserve every number, date, name, URL, and email. "
            "Do not use a forbidden keyword. Do not merge blocks. Return JSON with exactly one key, rewrites, containing objects with source_id and text."
        )
        payload = self._complete_json(
            system,
            {
                "prompt_version": OPTIMIZATION_PROMPT_VERSION,
                "supported_keywords": supported_keywords,
                "forbidden_keywords": forbidden_keywords,
                "blocks": [{"source_id": block["id"], "text": block["text"]} for block in blocks],
            },
        )
        rewrites = payload.get("rewrites")
        if not isinstance(rewrites, list):
            raise ProviderError("The AI service returned an invalid rewrite structure.")
        result: dict[str, str] = {}
        for item in rewrites:
            if not isinstance(item, dict) or not isinstance(item.get("source_id"), str) or not isinstance(item.get("text"), str):
                raise ProviderError("The AI service returned an invalid rewrite item.")
            if item["source_id"] in result:
                raise ProviderError("The AI service returned duplicate source references.")
            result[item["source_id"]] = item["text"].strip()
        return result


def provider_from_settings(settings: Settings) -> OpenAIProvider | None:
    if not settings.openai_api_key:
        return None
    return OpenAIProvider(
        api_key=settings.openai_api_key,
        api_base=settings.openai_api_base,
        model=settings.openai_model,
        timeout_seconds=settings.openai_timeout_seconds,
    )
