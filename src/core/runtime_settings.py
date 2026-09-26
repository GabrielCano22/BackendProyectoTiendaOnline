"""Configuración de ejecución derivada de variables de entorno."""


def should_run_startup_initialization(
    *, vercel: bool, configured: str | None
) -> bool:
    """Controla las tareas de inicialización que escriben en la base de datos."""
    if configured is None:
        return not vercel
    return configured.strip().lower() in {"1", "true", "yes", "si", "sí", "on"}
