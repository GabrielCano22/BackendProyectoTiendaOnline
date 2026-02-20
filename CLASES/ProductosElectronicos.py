#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/ProductosElectronicos.py
"""

from CLASES.Producto import Producto


class ProductosElectronicos(Producto):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        marca: str,
        precio: float,
        stock: int,
        tipo_producto: str,
    ):
        """
        Args:
            tipo_producto (str): Tipo de producto electrónico (ej: "televisor", "computadora", "celular").
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.tipo_producto = tipo_producto

    def obtener_info(self) -> str:
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Tipo de producto: {self.tipo_producto}"
        )

    def _atributos_extra(self) -> list:
        return [("TIPO DE PRODUCTO", self.tipo_producto)]

    def __str__(self) -> str:
        return self.obtener_info()
