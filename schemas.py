"""
Schemas Pydantic — La Tienda de Gerardo
"""
 
from datetime import datetime
from typing import Optional
from uuid import UUID
 
from pydantic import BaseModel, EmailStr
 
 
# ─────────────────────────── USUARIO (Gabriel) ────────────────────────────
 
class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None
 
 
class UsuarioCreate(UsuarioBase):
    contrasena: str
    rol: str = "cliente"  # "cliente" | "administrador"
 
 
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
 
 
class CambioContrasena(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str
 
 
class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    rol: str
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
 
    class Config:
        from_attributes = True
 
 
class LoginRequest(BaseModel):
    nombre_usuario: str
    contrasena: str
 
 
class LoginResponse(BaseModel):
    clave: str
    nombre_usuario: UsuarioResponse
 
 
# ─────────────────────────── CATEGORIA (Kevin) ────────────────────────────
# Kevin: agrega aqui CategoriaBase, CategoriaCreate, CategoriaUpdate, CategoriaResponse
 
 
# ─────────────────────────── PRODUCTO (Kevin) ────────────────────────────
# Kevin: agrega aqui ProductoBase, ProductoCreate, ProductoUpdate, ProductoResponse
 
 
# ─────────────────────────── DESCUENTO (Kevin) ────────────────────────────
# Kevin: agrega aqui DescuentoBase, DescuentoCreate, DescuentoUpdate, DescuentoResponse
 
 
# ─────────────────────────── TIENDA / CATALOGO (Kevin) ────────────────────────────
# Kevin: agrega aqui TiendaResponse, CatalogoResponse
 
 
# ─────────────────────────── CARRITO (Sebas) ────────────────────────────
# Sebas: agrega aqui AgregarAlCarritoRequest, CarritoResponse, DetalleCarritoResponse
 
 
# ─────────────────────────── FACTURA (Sebas) ────────────────────────────
# Sebas: agrega aqui FacturaResponse, DetalleFacturaResponse
 
 
# ─────────────────────────── RESPUESTA API (Sebas) ────────────────────────────
# Sebas: agrega aqui RespuestaAPI (o importarla de src.core.responses)