import uuid

from sqlalchemy import Column, DateTime, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class DetalleCarrito(Base):
    __tablename__ = "detalle_carritos"

    id_detalle_carrito = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_carrito = Column(
        UUID(as_uuid=True), ForeignKey("carritos.id_carrito"), nullable=False
    )

    id_producto = Column(
        UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False
    )

    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    carrito = relationship("Carrito", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_carrito")

    def __repr__(self):
        return f"<DetalleCarrito(id={self.id_detalle_carrito}, producto={self.id_producto}, cantidad={self.cantidad})>"
