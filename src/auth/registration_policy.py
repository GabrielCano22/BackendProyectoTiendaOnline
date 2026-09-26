"""Políticas de autorización para el registro público."""


def public_registration_role(_requested_role: str | None) -> str:
    """Un registro anónimo nunca puede elevar privilegios."""
    return "cliente"
