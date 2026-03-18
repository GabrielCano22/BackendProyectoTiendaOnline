import uuid


from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nombre_completo = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    clave = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
    es_admin = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    productos_creados = relationship(
        "Producto",
        back_populates="usuario_creacion",
        foreign_keys="Producto.id_usuario_creacion",
    )

    carritos = relationship("Carrito", back_populates="usuario")
    facturas = relationship("Factura", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nombre='{self.nombre_completo}', email='{self.email}')>"
