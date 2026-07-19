from __future__ import annotations

import unittest

from app.errors import ValidationError
from app.extractors import extract_cv
from tests.helpers import SAMPLE_CV_PARAGRAPHS, make_docx


class ExtractorTests(unittest.TestCase):
    def test_docx_extracts_source_blocks_and_sections(self) -> None:
        result = extract_cv("resume.docx", make_docx(SAMPLE_CV_PARAGRAPHS), max_bytes=5_242_880)
        self.assertIn("Python REST APIs", result.text)
        self.assertTrue(result.sections["experience"])
        self.assertTrue(result.sections["education"])
        self.assertEqual(len({block.id for block in result.blocks}), len(result.blocks))

    def test_extension_and_signature_must_agree(self) -> None:
        with self.assertRaisesRegex(ValidationError, "invalid signature"):
            extract_cv("resume.docx", b"not-a-zip", max_bytes=5_242_880)

    def test_non_english_cv_is_rejected(self) -> None:
        paragraphs = [
            "Özgeçmiş", "Yazılım Geliştirici", "Deneyim", "Bu projede takım ile birlikte uygulama geliştirme çalışmaları yaptım.",
            "Eğitim", "Bilgisayar mühendisliği eğitimi aldım ve çeşitli projelerde görev yaptım.", "Yetenekler", "Yazılım geliştirme ve veri yönetimi",
        ]
        with self.assertRaisesRegex(ValidationError, "English CV"):
            extract_cv("resume.docx", make_docx(paragraphs), max_bytes=5_242_880)

    def test_oversized_file_is_rejected_before_parsing(self) -> None:
        with self.assertRaisesRegex(ValidationError, "upload size limit"):
            extract_cv("resume.pdf", b"%PDF-" + b"0" * 200, max_bytes=100)


if __name__ == "__main__":
    unittest.main()

