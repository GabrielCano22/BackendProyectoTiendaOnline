#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: Tienda.py
"""
from CLASES.Producto import Producto
from CLASES.Alimentos import Alimentos
from CLASES.ProductosElectronicos import ProductosElectronicos
from CLASES.Ropa import Ropa
from CLASES.Hogar import Hogar
from CLASES.Mascotas import Mascotas
from CLASES.CuidadoPersonal import CuidadoPersonal
from CLASES.Bebes import Bebes
from CLASES.Licoreria import Licoreria


class Tienda:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.__catalogo: dict = {}

    def agregar_producto(self, producto: Producto) -> str:
        """Agrega un producto al catálogo."""
        if producto.codigo not in self.__catalogo:
            self.__catalogo[producto.codigo] = producto
            return f"Producto '{producto.nombre}' registrado exitosamente"
        else:
            return f"Ya existe un producto con el código {producto.codigo}."

    def eliminar_producto(self, codigo: str) -> str:
        """Elimina un producto del catálogo por su código."""
        if codigo in self.__catalogo:
            nombre: str = self.__catalogo[codigo].nombre
            del self.__catalogo[codigo]
            return f"Producto '{nombre}' eliminado del catálogo"
        else:
            return f"No se encontró ningún producto con el código {codigo}."

    def buscar_por_codigo(self, codigo: str) -> Producto:
        """Retorna el objeto producto o None si no existe."""
        return self.__catalogo.get(codigo, None)

    def obtener_catalogo(self) -> dict:
        """Retorna el diccionario completo del catálogo."""
        return self.__catalogo

    def mostrar_catalogo(self) -> None:
        """Muestra todos los productos disponibles en el catálogo."""
        if not self.__catalogo:
            print("\n  El catálogo está vacío.")
            return

        print(f"\n{'=' * 60}")
        print(f"  CATÁLOGO - {self.nombre.upper()}")
        print(f"{'=' * 60}")
        print(
            f"  {'CÓDIGO':<12} {'PRODUCTO':<25} {'MARCA':<12} {'PRECIO':>10} {'STOCK':>5}"
        )
        print(f"  {'-' * 58}")

        for producto in self.__catalogo.values():
            disponible: int = producto.obtener_stock()
            estado: str = str(disponible) if disponible > 0 else "Agotado"
            print(
                f"  {producto.codigo:<12} {producto.nombre:<25} "
                f"{producto.marca:<12} "
                f"${producto.obtener_precio():>9,.0f} {estado:>7}"
            )

        print(f"{'=' * 60}")
        print(f"  Total de productos: {len(self.__catalogo)}")

    def mostrar_detalle_producto(self, codigo: str) -> None:
        """Muestra el detalle completo de un producto."""
        producto: Producto = self.buscar_por_codigo(codigo)
        if producto:
            print(producto.mostrar_detalle())
        else:
            print(f"\n  No se encontró el producto con código {codigo}.")

    def buscar_producto(self, termino: str) -> None:
        """Busca productos por nombre o marca (búsqueda parcial)."""
        termino: str = termino.lower()
        hallados: list = []

        for producto in self.__catalogo.values():
            if termino in producto.nombre.lower() or termino in producto.marca.lower():
                hallados.append(producto)

        if hallados:
            print(f"\n  Resultados para '{termino}':")
            print(
                f"  {'CÓDIGO':<12} {'PRODUCTO':<25} {'MARCA':<12} {'PRECIO':>10} {'STOCK':>5}"
            )
            print(f"  {'-' * 58}")
            for p in hallados:
                print(
                    f"  {p.codigo:<12} {p.nombre:<25} "
                    f"{p.marca:<12} "
                    f"${p.obtener_precio():>9,.0f} {p.obtener_stock():>5}"
                )
        else:
            print(f"\n  No se encontraron productos con '{termino}'.")
