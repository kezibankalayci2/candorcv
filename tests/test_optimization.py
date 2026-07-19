from __future__ import annotations

import unittest

from app.analysis import analyze
from app.extractors import extract_cv
from app.jobs import normalize_job
from app.optimization import optimize_cv
from tests.helpers import SAMPLE_CV_PARAGRAPHS, SAMPLE_JOB, make_docx


class MaliciousProvider:
    model = "test-malicious"

    def rewrite_blocks(self, blocks, *, supported_keywords, forbidden_keywords):
        return {
            block["id"]: (
                block["text"] + " Led Kubernetes architecture for 500 enterprise systems."
                if "Python REST" in block["text"] else block["text"]
            )
            for block in blocks
        }


class OptimizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cv = extract_cv("resume.docx", make_docx(SAMPLE_CV_PARAGRAPHS), max_bytes=5_242_880).to_dict()
        self.job = normalize_job(SAMPLE_JOB, max_chars=30_000).to_dict()
        self.analysis = analyze(self.cv, self.job)

    def test_local_mode_preserves_every_source_block(self) -> None:
        content, references, model = optimize_cv(self.cv, self.analysis, None)
        self.assertEqual(model, "local-source-preserving-v1")
        self.assertEqual(len(references), len(self.cv["blocks"]))
        self.assertTrue(all(not reference["changed"] for reference in references))
        self.assertNotIn("Kubernetes", content)

    def test_unsupported_ai_claim_falls_back_to_original_line(self) -> None:
        content, references, _ = optimize_cv(self.cv, self.analysis, MaliciousProvider())
        self.assertNotIn("Kubernetes architecture", content)
        self.assertNotIn("500 enterprise", content)
        target = next(reference for reference in references if "Python REST" in reference["original"])
        self.assertEqual(target["optimized"], target["original"])


if __name__ == "__main__":
    unittest.main()

