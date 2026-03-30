"""
Schemas Pydantic — La Tienda de Gerardo
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr
from src.core.responses import RespuestaAPI


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


class AgregarAlCarritoRequest(BaseModel):
    id_producto: UUID
    cantidad: int


class ActualizarCantidadRequest(BaseModel):
    cantidad: int


class DetalleCarritoResponse(BaseModel):
    id_detalle: UUID
    id_producto: UUID
    cantidad: int
    precio_unitario: Decimal

    class Config:
        from_attributes = True


class CarritoResponse(BaseModel):
    id_carrito: UUID
    id_usuario: UUID
    estado: str
    detalles: List[DetalleCarritoResponse] = []

    class Config:
        from_attributes = True


class DetalleFacturaResponse(BaseModel):
    id_detalle: UUID
    id_producto: UUID
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    nombre_producto: str
    marca_producto: str

    class Config:
        from_attributes = True


class FacturaResponse(BaseModel):
    id_factura: UUID
    id_usuario: UUID
    total_bruto: Decimal
    total_descuento: Decimal
    total_neto: Decimal
    estado: str
    fecha_creacion: datetime
    detalles: List[DetalleFacturaResponse] = []

    class Config:
        from_attributes = True
