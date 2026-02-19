#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/cuidado_personal.py
"""

from CLASES.Producto import Producto


class CuidadoPersonal(Producto):
    def __init__(self, codigo: str, nombre: str, marca: str,
                 precio: float, stock: int, tipo_cuidado: str, genero: str) -> None:
        """
        Args:
            tipo_cuidado : Tipo de producto (ej: Cabello, Facial, Corporal, Dental)
            genero       : Género al que va dirigido (ej: Hombre, Mujer, Unisex)
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.tipo_cuidado: str = tipo_cuidado
        self.genero:       str = genero

    def obtener_info(self) -> str:
        return (f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
                f"| Tipo: {self.tipo_cuidado} | Género: {self.genero}")

    def _atributos_extra(self) -> list:
        return [
            ("TIPO",   self.tipo_cuidado),
            ("GÉNERO", self.genero)
        ]

    def __str__(self) -> str:
        return self.obtener_info()