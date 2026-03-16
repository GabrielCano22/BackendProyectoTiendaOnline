#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: src/entities/descuento.py
"""

import uuid
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base

class Descuento(Base):
    """
    Reglas de descuento por volumen de compra.
    Ejemplo: 3 o más unidades → 15%, 5 o más → 30%.
    """

    __tablename__ = "descuentos"
    id_descuento = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    descripcion = Column(String(100), nullable=False)
    unidades_minimas = Column(Integer, nullable=False)
    porcentaje = Column(Numeric(5, 2), nullable=False)
    def __repr__(self):
        return (
            f"<Descuento(descripcion='{self.descripcion}', "
            f"unidades_minimas={self.unidades_minimas}, "
            f"porcentaje={self.porcentaje}%)>"
        )