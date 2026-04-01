import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base

class Carrito(Base):
    __tablename__ = "carritos"

    id_carrito = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    estado = Column(String(20), default="activo")  # activo, finalizado, cancelado

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    usuario = relationship("Usuario", back_populates="carritos")
    detalles = relationship("DetalleCarrito", back_populates="carrito")

    def __repr__(self):
        return f"<Carrito(id={self.id_carrito}, usuario={self.id_usuario}, estado='{self.estado}')>"