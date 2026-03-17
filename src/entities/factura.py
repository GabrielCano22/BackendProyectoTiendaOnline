import uuid

from sqlalchemy import Column, DateTime, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Factura(Base):
    __tablename__ = "facturas"

    id_factura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    id_carrito = Column(
        UUID(as_uuid=True), ForeignKey("carritos.id_carrito"), nullable=False
    )

    total_bruto = Column(Numeric(10, 2), nullable=False)  # Antes del descuento
    porcentaje_descuento = Column(Numeric(5, 2), default=0)  # Ej: 15.00
    total_descuento = Column(Numeric(10, 2), default=0)  # Valor descontado
    total_neto = Column(Numeric(10, 2), nullable=False)  # Total final a pagar

    estado = Column(String(20), default="pendiente")  # pendiente, pagada, anulada

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="facturas")
    carrito = relationship("Carrito")
    detalles = relationship("DetalleFactura", back_populates="factura")

    def __repr__(self):
        return f"<Factura(id={self.id_factura}, usuario={self.id_usuario}, total={self.total_neto}, estado='{self.estado}')>"
