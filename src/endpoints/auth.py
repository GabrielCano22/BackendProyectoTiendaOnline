"""
Endpoints de Autenticacion
"""
 
import secrets
 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
 
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
    token = secrets.token_hex(32)
    return LoginResponse(clave=token, nombre_usuario=usuario)
 
 
@router.post("/registrar", response_model=UsuarioResponse, status_code=201)
async def registrar(data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario (cliente o administrador)."""
    crud = UsuarioCRUD(db)
    try:
        if data.rol == "administrador":
            usuario = crud.crear_administrador(
                nombre=data.nombre,
                nombre_usuario=data.nombre_usuario,
                email=data.email,
                contrasena=data.contrasena,
                telefono=data.telefono,
            )
        else:
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
 
 
@router.post("/crear-admin", response_model=RespuestaAPI)
async def crear_admin_inicial(db: Session = Depends(get_db)):
    """Crea el usuario administrador inicial si no existe ninguno."""
    crud = UsuarioCRUD(db)
    if crud.hay_administradores():
        return RespuestaAPI(
            mensaje="Ya existe al menos un administrador",
            exito=True,
            datos={"admin_existe": True},
        )
    contrasena = "Admin123!"
    try:
        admin = crud.crear_administrador(
            nombre="Administrador",
            nombre_usuario="admin",
            email="admin@tienda.com",
            contrasena=contrasena,
        )
        return RespuestaAPI(
            mensaje="Administrador creado exitosamente",
            exito=True,
            datos={
                "id": str(admin.id_usuario),
                "nombre_usuario": admin.nombre_usuario,
                "contrasena_temporal": contrasena,
            },
        )
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