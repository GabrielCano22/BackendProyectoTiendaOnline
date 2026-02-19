#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: CLASES/producto.py
"""

class Producto:
    def __init__(self, codigo, nombre, marca, precio, stock):
        """
        Args:
            codigo : Código único del producto (ej: "ALI-001")
            nombre : Nombre descriptivo del producto
            marca  : Marca del producto
            precio : Precio de venta en COP (atributo privado)
            stock  : Cantidad disponible en inventario (atributo privado)
        """
        self.codigo   = codigo
        self.nombre   = nombre
        self.marca    = marca
        self.__precio = precio 
        self.__stock  = stock    

    def obtener_precio(self):
        return self.__precio

    def cambiar_precio(self, nuevo_precio):
        if nuevo_precio > 0:
            self.__precio = nuevo_precio
            return f"Precio actualizado a ${nuevo_precio:,.0f} COP"
        else:
            return "Error: el precio debe ser mayor a 0$"

    def obtener_stock(self):
        return self.__stock

    def agregar_stock(self, cantidad):
        if cantidad > 0:
            self.__stock += cantidad
            return f"Stock actualizado. Ahora hay {self.__stock} unidades"
        else:
            return "Error: la cantidad debe ser mayor a 0"

    def reducir_stock(self, cantidad):
        if cantidad > 0 and cantidad <= self.__stock:
            self.__stock -= cantidad
            return True   
        else:
            return False   

    def obtener_info(self):
        """Retorna información básica. 
        Cada subclase puede sobreescribirlo.
        """
        return f"[{self.codigo}] {self.nombre} | Marca: {self.marca}"

    def _atributos_extra(self):
        """
        Método pensado para que cada subclase retorne sus atributos especiales
        como una lista de tuplas (etiqueta, valor).
        Ejemplo: [("TALLA", "M"), ("COLOR", "Rojo")]
        """
        return []

    def mostrar_detalle(self):
        """
        Muestra el detalle completo del producto.
        Las subclases amplían el detalle sobreescribiendo _atributos_extra().
        """
        lineas = []
        lineas.append("=" * 50)
        lineas.append(f"  CÓDIGO   : {self.codigo}")
        lineas.append(f"  PRODUCTO : {self.nombre}")
        lineas.append(f"  MARCA    : {self.marca}")
        lineas.append(f"  PRECIO   : ${self.__precio:,.0f} PESOS COLOMBIANOS")
        lineas.append(f"  STOCK    : {self.__stock} unidades")

        for etiqueta, valor in self._atributos_extra():
            lineas.append(f"  {etiqueta:<10}: {valor}")

        lineas.append("=" * 50)
        return "\n" + "\n".join(lineas)

    def esta_disponible(self):
        """Verifica si hay stock disponible."""
        return self.__stock > 0

    def __str__(self):
        return self.obtener_info()