#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/licoreria.py
"""

from CLASES.Producto import Producto


class Licoreria(Producto):
    def __init__(self, codigo, nombre, marca, precio, stock, tipo_licor):
        """
        Args:
            tipo_licor (str): Tipo de licor (ej: "vino", "cerveza", "whisky").
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.tipo_licor = tipo_licor

    def obtener_info(self):
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Tipo de licor: {self.tipo_licor}"
        )

    def _atributos_extra(self):
        return [("TIPO DE LICOR", self.tipo_licor)]

    def __str__(self):
        return self.obtener_info()
