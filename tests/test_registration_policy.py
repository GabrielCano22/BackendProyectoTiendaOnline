import unittest

from src.auth.registration_policy import public_registration_role


class RegistrationPolicyTests(unittest.TestCase):
    def test_public_registration_is_always_a_client(self):
        self.assertEqual(public_registration_role("cliente"), "cliente")
        self.assertEqual(public_registration_role("administrador"), "cliente")
        self.assertEqual(public_registration_role("ADMINISTRADOR"), "cliente")


if __name__ == "__main__":
    unittest.main()
