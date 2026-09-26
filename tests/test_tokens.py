import os
import time
import unittest
from unittest.mock import patch

from src.auth.tokens import InvalidTokenError, create_access_token, decode_access_token


class AccessTokenTests(unittest.TestCase):
    def test_round_trip_preserves_user_id(self):
        token = create_access_token("user-123", secret="test-secret", expires_in=60)

        payload = decode_access_token(token, secret="test-secret")

        self.assertEqual(payload["sub"], "user-123")

    def test_rejects_tampered_token(self):
        token = create_access_token("user-123", secret="test-secret", expires_in=60)
        replacement = "A" if token[-1] != "A" else "B"

        with self.assertRaises(InvalidTokenError):
            decode_access_token(token[:-1] + replacement, secret="test-secret")

    def test_rejects_expired_token(self):
        token = create_access_token("user-123", secret="test-secret", expires_in=-1)

        with self.assertRaises(InvalidTokenError):
            decode_access_token(token, secret="test-secret")

    def test_requires_secret_when_not_passed_explicitly(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                create_access_token("user-123")


if __name__ == "__main__":
    unittest.main()
