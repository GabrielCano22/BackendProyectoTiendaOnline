#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: src/crud/tienda_crud.py
"""

from typing import Optional
from sqlalchemy.orm import Session
from src.entities.catalogo import Catalogo
from src.entities.tienda import Tienda

class TiendaCrud:
    def __init__(self, db: Session):
        self.db = db
    def obtener_tienda(self) -> Optional[Tienda]:
        """Retorna la tienda principal (solo existe una)."""
        return self.db.query(Tienda).first()
    def obtener_catalogo(self) -> Optional[Catalogo]:
        """Retorna el catálogo asociado a la tienda principal."""
        tienda = self.obtener_tienda()
        if not tienda:
            return None
        return (
            self.db.query(Catalogo)
            .filter(Catalogo.id_tienda == tienda.id_tienda)
            .first()
        )
    def inicializar(self, nombre_tienda: str = "La Tienda de Gerardo") -> Tienda:
        """
        Crea la tienda y su catálogo si aún no existen.
        Se llama una sola vez al arrancar el sistema.
        """
        tienda = self.obtener_tienda()
        if tienda:
            return tienda
        tienda = Tienda(nombre=nombre_tienda)
        self.db.add(tienda)
        self.db.flush()
        catalogo = Catalogo(
            id_tienda=tienda.id_tienda,
            descripcion=f"Catálogo oficial de {nombre_tienda}",
        )
        self.db.add(catalogo)
        self.db.commit()
        self.db.refresh(tienda)
        return tienda