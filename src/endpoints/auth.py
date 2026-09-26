"""
Endpoints de Autenticacion
"""
 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.registration_policy import public_registration_role
from src.auth.tokens import create_access_token
from src.crud.usuario_crud import UsuarioCRUD
from src.database.config import get_db
from src.core.responses import RespuestaAPI
from schemas import LoginRequest, LoginResponse, UsuarioCreate, UsuarioResponse
 
router = APIRouter(prefix="/auth", tags=["autenticacion"])
 
@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Autenticar usuario. Devuelve token de sesion y datos del usuario."""
    crud = UsuarioCRUD(db)
    usuario = crud.autenticar(login_data.nombre_usuario, login_data.contrasena)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas o usuario inactivo",
        )
    token = create_access_token(str(usuario.id_usuario))
    return LoginResponse(clave=token, nombre_usuario=usuario)
 
@router.post("/registrar", response_model=UsuarioResponse, status_code=201)
async def registrar(data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo cliente."""
    crud = UsuarioCRUD(db)
    try:
        registration_role = public_registration_role(data.rol)
        if registration_role == "cliente":
            usuario = crud.crear_cliente(
                nombre=data.nombre,
                nombre_usuario=data.nombre_usuario,
                email=data.email,
                contrasena=data.contrasena,
                telefono=data.telefono,
            )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
 
@router.get("/estado", response_model=RespuestaAPI)
async def estado():
    """Estado del sistema de autenticacion."""
    return RespuestaAPI(
        mensaje="Sistema de autenticacion activo",
        exito=True,
        datos={"version": "1.0.0"},
    )
