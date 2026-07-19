from __future__ import annotations

import unittest

from app.errors import ValidationError
from app.jobs import normalize_job
from tests.helpers import SAMPLE_JOB


class JobTests(unittest.TestCase):
    def test_job_sections_are_normalized(self) -> None:
        job = normalize_job(SAMPLE_JOB, max_chars=30_000)
        self.assertEqual(job.title, "Backend Software Engineer")
        self.assertTrue(job.required)
        self.assertTrue(job.preferred)
        self.assertTrue(job.responsibilities)

    def test_short_job_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            normalize_job("Python engineer", max_chars=30_000)


if __name__ == "__main__":
    unittest.main()

