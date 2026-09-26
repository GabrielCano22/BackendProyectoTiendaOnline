import unittest

from src.core.runtime_settings import should_run_startup_initialization


class RuntimeSettingsTests(unittest.TestCase):
    def test_startup_initialization_is_disabled_by_default_on_vercel(self):
        self.assertFalse(should_run_startup_initialization(vercel=True, configured=None))

    def test_startup_initialization_is_enabled_by_default_outside_vercel(self):
        self.assertTrue(should_run_startup_initialization(vercel=False, configured=None))

    def test_explicit_startup_setting_wins(self):
        self.assertTrue(should_run_startup_initialization(vercel=True, configured="true"))
        self.assertFalse(should_run_startup_initialization(vercel=False, configured="false"))


if __name__ == "__main__":
    unittest.main()
