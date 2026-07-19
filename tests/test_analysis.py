from __future__ import annotations

import unittest

from app.analysis import analyze, validate_analysis
from app.extractors import extract_cv
from app.jobs import normalize_job
from tests.helpers import SAMPLE_CV_PARAGRAPHS, SAMPLE_JOB, make_docx


class AnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cv = extract_cv("resume.docx", make_docx(SAMPLE_CV_PARAGRAPHS), max_bytes=5_242_880).to_dict()
        self.job = normalize_job(SAMPLE_JOB, max_chars=30_000).to_dict()

    def test_analysis_is_explainable_and_bounded(self) -> None:
        result = analyze(self.cv, self.job)
        validate_analysis(result, self.cv)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertTrue(result["strengths"])
        self.assertTrue(all(item["source"]["source_id"].startswith("cv-") for item in result["strengths"]))

    def test_job_only_keyword_is_not_supported(self) -> None:
        result = analyze(self.cv, self.job)
        statuses = {item["term"]: item["status"] for item in result["keywords"]}
        self.assertEqual(statuses["Kubernetes"], "not_visible")
        self.assertEqual(statuses["AWS"], "not_visible")

    def test_missing_does_not_claim_candidate_lacks_skill(self) -> None:
        result = analyze(self.cv, self.job)
        kubernetes = next(item for item in result["missing_areas"] if item["title"] == "Kubernetes")
        self.assertIn("not visible", kubernetes["detail"])
        self.assertIn("does not mean", kubernetes["detail"])


if __name__ == "__main__":
    unittest.main()

