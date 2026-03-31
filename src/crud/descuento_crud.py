#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: src/crud/descuento_crud.py
"""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.descuento import Descuento

class DescuentoCrud:
    def __init__(self, db: Session):
        self.db = db

    def crear(
        self, descripcion: str, unidades_minimas: int, porcentaje: Decimal
    ) -> Descuento:
        """Crea una nueva regla de descuento."""
        if unidades_minimas < 1:
            raise ValueError("Las unidades mínimas deben ser al menos 1")
        if not (0 < porcentaje <= 100):
            raise ValueError("El porcentaje debe estar entre 1 y 100")
        descuento = Descuento(
            descripcion=descripcion.strip(),
            unidades_minimas=unidades_minimas,
            porcentaje=porcentaje,
        )
        self.db.add(descuento)
        self.db.commit()
        self.db.refresh(descuento)
        return descuento

    def obtener_por_id(self, id_descuento: UUID) -> Optional[Descuento]:
        """Busca un descuento por su UUID."""
        return (
            self.db.query(Descuento)
            .filter(Descuento.id_descuento == id_descuento)
            .first()
        )

    def listar(self) -> List[Descuento]:
        """Lista todos los descuentos ordenados por unidades mínimas."""
        return self.db.query(Descuento).order_by(Descuento.unidades_minimas).all()

    def actualizar(self, id_descuento: UUID, **kwargs) -> Optional[Descuento]:
        """Actualiza los campos indicados de un descuento existente."""
        descuento = self.obtener_por_id(id_descuento)
        if not descuento:
            return None
        for key, value in kwargs.items():
            if hasattr(descuento, key):
                setattr(descuento, key, value)
        self.db.commit()
        self.db.refresh(descuento)
        return descuento

    def eliminar(self, id_descuento: UUID) -> bool:
        """Elimina un descuento de la base de datos."""
        descuento = self.obtener_por_id(id_descuento)
        if not descuento:
            return False
        self.db.delete(descuento)
        self.db.commit()
        return True

    def aplicar_descuento(self, total_unidades: int) -> Decimal:
        """
        Retorna el porcentaje de descuento que corresponde
        según el total de unidades en el carrito.
        Si no aplica ninguna regla, retorna 0.
        """
        descuentos = self.listar()
        porcentaje_aplicable = Decimal("0")
        for d in sorted(descuentos, key=lambda x: x.unidades_minimas, reverse=True):
            if total_unidades >= d.unidades_minimas:
                porcentaje_aplicable = d.porcentaje
                break
        return porcentaje_aplicable

    def seed_descuentos_base(self) -> None:
        """
        Inserta los descuentos por defecto si la tabla está vacía.
        Se llama al iniciar el sistema.
        - 3 o más unidades → 15%
        - 5 o más unidades → 30%
        """
        if self.db.query(Descuento).count() == 0:
            self.crear("Descuento por 3 o más unidades", 3, Decimal("15.00"))
            self.crear("Descuento por 5 o más unidades", 5, Decimal("30.00"))
