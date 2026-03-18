import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Producto(Base):
    """Modelo de Productos"""

    __tablename__ = "productos"

    id_producto = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo_producto = Column(String(50), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    marca = Column(String(100), nullable=False)

    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    eliminado = Column(Boolean, default=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    categoria_id = Column(
        UUID(as_uuid=True), ForeignKey("categorias.id_categoria"), nullable=False
    )
    id_catalogo = Column(
        UUID(as_uuid=True), ForeignKey("catalogos.id_catalogo"), nullable=True
    )
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    categoria = relationship("Categoria", back_populates="productos")
    catalogo = relationship("Catalogo", back_populates="productos")
   

    usuario_creacion = relationship(
        "Usuario",
        foreign_keys=[id_usuario_creacion],
    )
    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuario_edita],
    )
    detalles_carrito = relationship("DetalleCarrito", back_populates="producto")
    detalles_factura = relationship("DetalleFactura", back_populates="producto")

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, nombre='{self.nombre}', precio={self.precio})>"
