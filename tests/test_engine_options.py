import unittest

from sqlalchemy.pool import NullPool

from src.database.engine_options import build_engine_options


class EngineOptionsTests(unittest.TestCase):
    def test_serverless_uses_null_pool(self):
        options = build_engine_options(serverless=True)

        self.assertIs(options["poolclass"], NullPool)
        self.assertNotIn("pool_size", options)
        self.assertNotIn("max_overflow", options)

    def test_long_lived_process_keeps_bounded_pool(self):
        options = build_engine_options(serverless=False)

        self.assertEqual(options["pool_size"], 5)
        self.assertEqual(options["max_overflow"], 5)
        self.assertEqual(options["pool_recycle"], 300)


if __name__ == "__main__":
    unittest.main()
