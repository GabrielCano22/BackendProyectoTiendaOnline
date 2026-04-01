"""
Dependencias de autenticacion y autorizacion
"""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.usuario import Usuario

# Almacen de sesiones en memoria: token -> id_usuario (str)
_sesiones: dict[str, str] = {}

_bearer = HTTPBearer()


def registrar_sesion(token: str, id_usuario: UUID) -> None:
    _sesiones[token] = str(id_usuario)


def cerrar_sesion(token: str) -> None:
    _sesiones.pop(token, None)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    token = credentials.credentials
    id_str = _sesiones.get(token)
    if not id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o sesion expirada",
        )
    from src.crud.usuario_crud import UsuarioCRUD
    usuario = UsuarioCRUD(db).obtener_por_id(UUID(id_str))
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo",
        )
    return usuario


def require_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    if usuario.rol != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requiere rol de administrador",
        )
    return usuario