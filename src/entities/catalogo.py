#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: src/entities/catalogo.py
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base

class Catalogo(Base):
    """Catálogo de productos asociado a la tienda. Relación 1:1 con Tienda."""

    __tablename__ = "catalogos"
    id_catalogo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_tienda = Column(
        UUID(as_uuid=True),
        ForeignKey("tiendas.id_tienda"),
        nullable=False,
        unique=True,
    )
    descripcion = Column(String(255), nullable=True)
    tienda = relationship("Tienda", back_populates="catalogo")
    productos = relationship("Producto", back_populates="catalogo")
    def __repr__(self):
        return f"<Catalogo(id='{self.id_catalogo}')>"