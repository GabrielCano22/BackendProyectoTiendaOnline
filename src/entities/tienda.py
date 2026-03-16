#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: src/entities/tienda.py
"""

import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base

class Tienda(Base):
    """Entidad raíz del sistema. Solo existe una tienda."""

    __tablename__ = "tiendas"
    id_tienda = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(150), nullable=False, unique=True)
    catalogo = relationship("Catalogo", back_populates="tienda", uselist=False)
    def __repr__(self):
        return f"<Tienda(nombre='{self.nombre}')>"