#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/Producto.py
"""


class Producto:
    def __init__(
        self, codigo: str, nombre: str, marca: str, precio: float, stock: int
    ) -> None:
        """
        Args:
            codigo : Código único del producto (ej: "ALI-001")
            nombre : Nombre descriptivo del producto
            marca  : Marca del producto
            precio : Precio de venta en COP (atributo privado)
            stock  : Cantidad disponible en inventario (atributo privado)
        """
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.marca: str = marca
        self.__precio: float = precio
        self.__stock: int = stock

    def obtener_precio(self) -> float:
        return self.__precio

    def cambiar_precio(self, nuevo_precio: float) -> str:
        if nuevo_precio > 0:
            self.__precio = nuevo_precio
            return f"Precio actualizado a ${nuevo_precio:,.0f} COP"
        else:
            return "Error: el precio debe ser mayor a 0"

    def obtener_stock(self) -> int:
        return self.__stock

    def agregar_stock(self, cantidad: int) -> str:
        if cantidad > 0:
            self.__stock += cantidad
            return f"Stock actualizado. Ahora hay {self.__stock} unidades"
        else:
            return "Error: la cantidad debe ser mayor a 0"

    def reducir_stock(self, cantidad: int) -> bool:
        if cantidad > 0 and cantidad <= self.__stock:
            self.__stock -= cantidad
            return True
        else:
            return False

    def obtener_info(self) -> str:
        """Retorna información básica. Cada subclase puede sobreescribirlo."""
        return f"[{self.codigo}] {self.nombre} | Marca: {self.marca}"

    def _atributos_extra(self) -> list:
        """
        Método pensado para que cada subclase retorne sus atributos especiales
        como una lista de tuplas (etiqueta, valor).
        Ejemplo: [("TALLA", "M"), ("COLOR", "Rojo")]
        """
        return []

    def mostrar_detalle(self) -> str:
        """
        Muestra el detalle completo del producto.
        Las subclases amplían el detalle sobreescribiendo _atributos_extra().
        """
        lineas: list = []
        lineas.append("=" * 50)
        lineas.append(f"  CÓDIGO   : {self.codigo}")
        lineas.append(f"  PRODUCTO : {self.nombre}")
        lineas.append(f"  MARCA    : {self.marca}")
        lineas.append(f"  PRECIO   : ${self.__precio:,.0f} COP")
        lineas.append(f"  STOCK    : {self.__stock} unidades")

        for etiqueta, valor in self._atributos_extra():
            lineas.append(f"  {etiqueta:<10}: {valor}")

        lineas.append("=" * 50)
        return "\n" + "\n".join(lineas)

    def esta_disponible(self) -> bool:
        """Verifica si hay stock disponible para este producto."""
        return self.__stock > 0

    def __str__(self) -> str:
        return self.obtener_info()
