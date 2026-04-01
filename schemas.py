"""
Schemas Pydantic — La Tienda de Gerardo
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr
from src.core.responses import RespuestaAPI

class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    contrasena: str
    rol: str = "cliente"

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

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class CategoriaResponse(CategoriaBase):
    id_categoria: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None

    class Config:
        from_attributes = True

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_producto: str
    codigo: str
    marca: str
    precio: Decimal
    stock: int = 0

class ProductoCreate(ProductoBase):
    categoria_id: UUID

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_producto: Optional[str] = None
    marca: Optional[str] = None
    precio: Optional[Decimal] = None
    stock: Optional[int] = None

class ProductoResponse(ProductoBase):
    id_producto: UUID
    categoria_id: UUID
    id_catalogo: Optional[UUID] = None
    eliminado: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None

    class Config:
        from_attributes = True

class DescuentoBase(BaseModel):
    descripcion: str
    unidades_minimas: int
    porcentaje: Decimal

class DescuentoCreate(DescuentoBase):
    pass

class DescuentoUpdate(BaseModel):
    descripcion: Optional[str] = None
    unidades_minimas: Optional[int] = None
    porcentaje: Optional[Decimal] = None

class DescuentoResponse(DescuentoBase):
    id_descuento: UUID

    class Config:
        from_attributes = True

class TiendaResponse(BaseModel):
    id_tienda: UUID
    nombre: str

    class Config:
        from_attributes = True

class CatalogoResponse(BaseModel):
    id_catalogo: UUID
    id_tienda: UUID
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

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
    id_detalle_factura: UUID
    id_producto: UUID
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    nombre_producto: str

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