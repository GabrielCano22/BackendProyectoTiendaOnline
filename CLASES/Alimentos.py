#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/Alimentos.py
"""

from CLASES.Producto import Producto


class Alimentos(Producto):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        marca: str,
        precio: float,
        stock: int,
        categoria_alimento: str,
    ) -> None:
        """
        Args:
            categoria_alimento : Categoría del alimento (ej: Granos, Lácteos, Carnes)
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.categoria_alimento: str = categoria_alimento

    def obtener_info(self) -> str:
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Categoría: {self.categoria_alimento}"
        )

    def _atributos_extra(self) -> list:
        return [("CATEGORÍA", self.categoria_alimento)]

    def __str__(self) -> str:
        return self.obtener_info()
