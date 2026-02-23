#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/Licoreria.py
"""

from CLASES.Producto import Producto


class Licoreria(Producto):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        marca: str,
        precio: float,
        stock: int,
        tipo_licor: str,
    ) -> None:
        """
        Args:
            tipo_licor (str): Tipo de licor (ej: "vino", "cerveza", "whisky").
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.tipo_licor = tipo_licor

    def obtener_info(self) -> str:
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Tipo de licor: {self.tipo_licor}"
        )

    def _atributos_extra(self) -> list:
        return [("TIPO DE LICOR", self.tipo_licor)]

    def __str__(self) -> str:
        return self.obtener_info()
