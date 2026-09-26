"""Configuración de ejecución derivada de variables de entorno."""


def cors_origins(configured: str | None) -> list[str]:
    """Devuelve orígenes CORS explícitos y sin valores vacíos."""
    if not configured:
        return ["http://localhost:4200"]
    return [origin.strip() for origin in configured.split(",") if origin.strip()]


def should_run_startup_initialization(
    *, vercel: bool, configured: str | None
) -> bool:
    """Controla las tareas de inicialización que escriben en la base de datos."""
    if configured is None:
        return not vercel
    return configured.strip().lower() in {"1", "true", "yes", "si", "sí", "on"}
