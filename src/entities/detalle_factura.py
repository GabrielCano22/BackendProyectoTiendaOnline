import uuid

from sqlalchemy import Column, DateTime, Integer, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base

class DetalleFactura(Base):
    __tablename__ = "detalle_facturas"

    id_detalle_factura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_factura = Column(
        UUID(as_uuid=True), ForeignKey("facturas.id_factura"), nullable=False
    )

    id_producto = Column(
        UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False
    )

    nombre_producto = Column(
        String(150), nullable=False
    )  
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    factura = relationship("Factura", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_factura")

    def __repr__(self):
        return f"<DetalleFactura(id={self.id_detalle_factura}, producto='{self.nombre_producto}', subtotal={self.subtotal})>"