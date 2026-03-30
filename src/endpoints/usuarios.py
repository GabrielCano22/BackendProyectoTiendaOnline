"""
Endpoints de Usuarios
"""
 
from typing import List
from uuid import UUID
 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
 
from src.auth.security import PasswordManager
from src.crud.usuario_crud import UsuarioCRUD
from src.database.config import get_db
from src.core.responses import RespuestaAPI
from schemas import CambioContrasena, UsuarioResponse, UsuarioUpdate
 
router = APIRouter(prefix="/usuarios", tags=["usuarios"])
 
 
@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    return crud.listar()
 
 
@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    u = crud.obtener_por_id(usuario_id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    return u
 
 
@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(usuario_id: UUID, data: UsuarioUpdate, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    campos = {k: v for k, v in data.dict().items() if v is not None}
    try:
        u = crud.actualizar(usuario_id, **campos)
        if not u:
            raise HTTPException(404, "Usuario no encontrado")
        return u
    except ValueError as e:
        raise HTTPException(400, str(e))
 
 
@router.patch("/{usuario_id}/desactivar", response_model=RespuestaAPI)
async def desactivar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    if not crud.desactivar(usuario_id):
        raise HTTPException(404, "Usuario no encontrado")
    return RespuestaAPI(mensaje="Usuario desactivado", exito=True)
 
 
@router.delete("/{usuario_id}", response_model=RespuestaAPI)
async def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    if not crud.eliminar(usuario_id):
        raise HTTPException(404, "Usuario no encontrado")
    return RespuestaAPI(mensaje="Usuario eliminado", exito=True)
 
 
@router.post("/{usuario_id}/cambiar-contrasena", response_model=RespuestaAPI)
async def cambiar_contrasena(usuario_id: UUID, data: CambioContrasena, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    u = crud.obtener_por_id(usuario_id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    if not PasswordManager.verify_password(data.contrasena_actual, u.contrasena_hash):
        raise HTTPException(400, "Contrasena actual incorrecta")
    valida, msg = PasswordManager.validate_password_strength(data.nueva_contrasena)
    if not valida:
        raise HTTPException(400, msg)
    crud.actualizar(usuario_id, contrasena_hash=PasswordManager.hash_password(data.nueva_contrasena))
    return RespuestaAPI(mensaje="Contrasena actualizada exitosamente", exito=True)