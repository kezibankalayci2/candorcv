from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.errors import NotFoundError, UnauthorizedError
from app.repository import Repository


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repository = Repository(Path(self.temp.name) / "test.db", 60)
        self.session_a = self.repository.create_session()
        self.session_b = self.repository.create_session()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_records_are_isolated_by_session(self) -> None:
        cv = self.repository.save_cv(
            self.session_a["id"],
            filename="a.docx",
            media_type="application/test",
            content_hash="hash",
            extracted={"text": "English CV content", "blocks": [], "sections": {}},
        )
        with self.assertRaises(NotFoundError):
            self.repository.get_cv(cv["id"], self.session_b["id"])

    def test_decision_is_scoped_to_analysis(self) -> None:
        cv = self.repository.save_cv(
            self.session_a["id"], filename="a.docx", media_type="application/test", content_hash="hash", extracted={}
        )
        job = self.repository.save_job(
            self.session_a["id"], content_hash="job", raw_text="job", structured={}
        )
        analysis = self.repository.save_analysis(
            self.session_a["id"],
            cv_id=cv["id"], job_id=job["id"], result={"score": 50},
            model_version="local", prompt_version="v1", scoring_version="v1",
        )
        decision = self.repository.save_decision(self.session_a["id"], analysis_id=analysis["id"], choice="no")
        self.assertEqual(decision["choice"], "no")
        self.assertEqual(self.repository.get_decision_for_analysis(analysis["id"], self.session_a["id"])["choice"], "no")

    def test_delete_session_cascades_all_records(self) -> None:
        cv = self.repository.save_cv(
            self.session_a["id"], filename="a.docx", media_type="application/test", content_hash="hash", extracted={}
        )
        self.repository.delete_session(self.session_a["id"])
        with self.assertRaises(UnauthorizedError):
            self.repository.get_cv(cv["id"], self.session_a["id"])


if __name__ == "__main__":
    unittest.main()
