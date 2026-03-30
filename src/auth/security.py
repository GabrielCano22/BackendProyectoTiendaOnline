"""
Modulo de seguridad para manejo de contrasenas
"""
 
import hashlib
import secrets
from typing import Tuple
 
class PasswordManager:
 
    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return f"{salt}:{password_hash.hex()}"
 
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        try:
            salt, hash_part = password_hash.split(":")
            check = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
            )
            return check.hex() == hash_part
        except (ValueError, AttributeError):
            return False
 
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        if len(password) < 8:
            return False, "La contrasena debe tener al menos 8 caracteres"
        if not any(c.isupper() for c in password):
            return False, "Debe contener al menos una letra mayuscula"
        if not any(c.islower() for c in password):
            return False, "Debe contener al menos una letra minuscula"
        if not any(c.isdigit() for c in password):
            return False, "Debe contener al menos un numero"
        return True, "Contrasena valida"