"""
Entidad Usuario con herencia — Cliente y Administrador
Usa Single Table Inheritance (STI) de SQLAlchemy
"""

import uuid

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
    rol = Column(String(20), nullable=False, default="cliente")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    __mapper_args__ = {
        "polymorphic_on": rol,
        "polymorphic_identity": "usuario",
    }

    productos_creados = relationship(
        "Producto",
        back_populates="usuario_creacion",
        foreign_keys="Producto.id_usuario_creacion",
    )
    carritos = relationship(
        "Carrito", back_populates="usuario", foreign_keys="Carrito.id_usuario"
    )
    facturas = relationship(
        "Factura", back_populates="usuario", foreign_keys="Factura.id_usuario"
    )

    def __repr__(self):
        return (
            f"<Usuario(id={self.id_usuario}, nombre='{self.nombre}', rol='{self.rol}')>"
        )

class Cliente(Usuario):
    """
    Subclase Cliente — hereda de Usuario.
    Tiene carrito e historial de compras.
    """

    historial = Column(Text, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "cliente",
    }

    def __repr__(self):
        return f"<Cliente(id={self.id_usuario}, nombre='{self.nombre}')>"

class Administrador(Usuario):
    """
    Subclase Administrador — hereda de Usuario.
    Tiene permisos para gestionar el catalogo.
    """

    __mapper_args__ = {
        "polymorphic_identity": "administrador",
    }

    def __repr__(self):
        return f"<Administrador(id={self.id_usuario}, nombre='{self.nombre}')>"