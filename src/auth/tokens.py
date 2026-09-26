"""Tokens de acceso firmados y verificables sin estado en memoria."""

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any


class InvalidTokenError(ValueError):
    """El token no tiene un formato, firma o vigencia válidos."""


def _secret(explicit_secret: str | None) -> str:
    value = explicit_secret or os.getenv("JWT_SECRET")
    if not value:
        raise RuntimeError("Se requiere JWT_SECRET en las variables de entorno")
    return value


def _encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def create_access_token(
    user_id: str,
    *,
    secret: str | None = None,
    expires_in: int = 60 * 60 * 24,
) -> str:
    """Crea un JWT HS256 con el identificador del usuario como sujeto."""
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": str(user_id), "iat": now, "exp": now + expires_in}
    header_part = _encode(json.dumps(header, separators=(",", ":")).encode())
    payload_part = _encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    signature = hmac.new(
        _secret(secret).encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    return f"{header_part}.{payload_part}.{_encode(signature)}"


def decode_access_token(token: str, *, secret: str | None = None) -> dict[str, Any]:
    """Valida un JWT HS256 y devuelve sus claims."""
    try:
        header_part, payload_part, signature_part = token.split(".")
        header = json.loads(_decode(header_part))
        payload = json.loads(_decode(payload_part))
        signature = _decode(signature_part)
    except (ValueError, TypeError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise InvalidTokenError("Token inválido") from exc

    if header.get("alg") != "HS256" or header.get("typ") != "JWT":
        raise InvalidTokenError("Algoritmo de token no permitido")

    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    expected = hmac.new(
        _secret(secret).encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    if not hmac.compare_digest(signature, expected):
        raise InvalidTokenError("Firma de token inválida")

    subject = payload.get("sub")
    expiration = payload.get("exp")
    if not isinstance(subject, str) or not subject:
        raise InvalidTokenError("Token sin sujeto")
    if not isinstance(expiration, int) or expiration <= int(time.time()):
        raise InvalidTokenError("Token expirado")
    return payload
