from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.config import load_settings


class ConfigTests(unittest.TestCase):
    def test_defaults_are_safe_for_local_development(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            settings = load_settings(Path(directory))
            self.assertEqual(settings.host, "127.0.0.1")
            self.assertEqual(settings.openai_model, "gpt-5.6-luna")
            self.assertIsNone(settings.openai_api_key)
            self.assertTrue(settings.analysis_enabled)
            self.assertTrue(settings.optimization_enabled)

    def test_production_rejects_default_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ,
            {"APP_ENV": "production", "APP_SECRET": "change-me-in-production"},
            clear=True,
        ):
            with self.assertRaises(ValueError):
                load_settings(Path(directory))

    def test_feature_flags_are_strict_booleans(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ,
            {"ANALYSIS_ENABLED": "false", "OPTIMIZATION_ENABLED": "maybe"},
            clear=True,
        ):
            with self.assertRaises(ValueError):
                load_settings(Path(directory))


if __name__ == "__main__":
    unittest.main()
