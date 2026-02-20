#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/mascotas.py
"""

from CLASES.Producto import Producto


class Mascotas(Producto):
    def __init__(self, codigo, nombre, marca, precio, stock, edad, tamano):
        """
        Args:
            edad (str): Etapa de edad recomendada
                (ej: "cachorro", "adulto", "senior").
            tamano (str): Tamaño recomendado
                (ej: "pequeño", "mediano", "grande").
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.edad = edad
        self.tamano = tamano

    def obtener_info(self):
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Edad: {self.edad} | Tamaño: {self.tamano}"
        )

    def _atributos_extra(self):
        return [("EDAD", self.edad), ("TAMAÑO", self.tamano)]

    def __str__(self):
        return self.obtener_info()
