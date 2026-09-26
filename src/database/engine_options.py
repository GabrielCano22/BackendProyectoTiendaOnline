"""Opciones del motor SQLAlchemy según el entorno de ejecución."""

from sqlalchemy.pool import NullPool


def build_engine_options(serverless: bool) -> dict:
    """Construye opciones seguras para procesos persistentes o serverless."""
    options: dict = {
        "echo": False,
        "pool_pre_ping": True,
    }

    if serverless:
        options["poolclass"] = NullPool
    else:
        options.update(
            pool_size=5,
            pool_recycle=300,
            max_overflow=5,
        )

    return options
