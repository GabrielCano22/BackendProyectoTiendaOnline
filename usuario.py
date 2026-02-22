#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: usuario.py
"""

from Carrito import Carrito
from tienda  import Tienda


class Usuario:

    def __init__(self, nombre: str, rol: str) -> None:
        self.nombre: str = nombre
        self.rol:str = rol

    def obtener_info(self) -> str:
        return f"Usuario: {self.nombre} | Rol: {self.rol}"

    def __str__(self) -> str:
        return self.obtener_info()

class Cliente(Usuario):
    def __init__(self, nombre: str) -> None:
        super().__init__(nombre, "Cliente")
        self.carrito:Carrito = Carrito()
        self.historial: list= []

    def obtener_info(self) -> str:
        return (f"Cliente: {self.nombre} | "
                f"Compras realizadas: {len(self.historial)}")

    def registrar_compra(self, resumen_compra: str) -> None:
        """Guarda el resumen de una compra en el historial del cliente."""
        self.historial.append(resumen_compra)

    def ver_historial(self) -> None:
        """Muestra el historial de compras del cliente."""
        if not self.historial:
            print("\n  No tienes compras registradas aún")
            return

        print(f"\n{'=' * 50}")
        print(f"  HISTORIAL DE COMPRAS - {self.nombre.upper()}")
        print(f"{'=' * 50}")
        for i, compra in enumerate(self.historial, 1):
            print(f"\n  Compra #{i}")
            print(compra)
        print(f"{'=' * 50}")

class Administrador(Usuario):
    def __init__(self, nombre: str) -> None:
        super().__init__(nombre, "Administrador")

    def obtener_info(self) -> str:
        return f"Administrador: {self.nombre}"

    def registrar_producto(self, tienda: Tienda) -> None:
        """
        Guía al administrador paso a paso para registrar
        un nuevo producto en el catálogo.
        """
        from CLASES.Alimentos            import Alimentos
        from CLASES.ProductosElectronicos import ProductosElectronicos
        from CLASES.Cuidado_Personal     import CuidadoPersonal
        from CLASES.Licoreria            import Licoreria
        from CLASES.Mascotas             import Mascotas
        from CLASES.Bebes                import Bebes
        from CLASES.hogar                import Hogar
        from CLASES.Ropa                 import Ropa
        
        print(f"\n{'=' * 50}")
        print("  REGISTRAR NUEVO PRODUCTO")
        print(f"{'=' * 50}")
        print("  1. Alimentos")
        print("  2. Productos Electrónicos")
        print("  3. Cuidado Personal")
        print("  4. Licorería")
        print("  5. Mascotas")
        print("  6. Bebés")
        print("  7. Hogar")
        print("  8. Ropa")
        print(f"{'=' * 50}")

        categoria: str = input("  Seleccione la categoría (1-8): ").strip()

        if categoria not in [str(i) for i in range(1,9)]:
            print("  Categoría no válida.")
            return

        print("\n  Complete los datos del producto:")
        codigo:     str = input("  Código (ej: ALI-003): ").strip().upper()
        nombre:     str = input("  Nombre del producto: ").strip()
        marca:      str = input("  Marca: ").strip()
        precio_str: str = input("  Precio (COP): ").strip()
        stock_str:  str = input("  Stock inicial: ").strip()

        if not precio_str.replace(".", "", 1).isdigit():
            print("  Error: el precio debe ser un número")
            return

        if not stock_str.isdigit():
            print("  Error: el stock debe ser un número entero")
            return

        precio: float = float(precio_str)
        stock:  int   = int(stock_str)

        if categoria == "1":
            categoria_alimento: str = input("  Categoría (ej: Granos, Lácteos): ").strip()
            nuevo = Alimentos(codigo, nombre, marca, precio, stock, categoria_alimento)

        elif categoria == "2":
            tipo_producto: str = input("  Tipo (ej: Televisor, Celular, Computadora): ").strip()
            nuevo = ProductosElectronicos(codigo, nombre, marca, precio, stock, tipo_producto)

        elif categoria == "3":
            tipo_cuidado: str = input("  Tipo (ej: Cabello, Facial): ").strip()
            genero:       str = input("  Género (Hombre, Mujer, Unisex): ").strip()
            nuevo = CuidadoPersonal(codigo, nombre, marca, precio, stock, tipo_cuidado, genero)

        elif categoria == "4":
            tipo_licor: str = input("  Tipo (ej: Aguardiente, Cerveza, Vino): ").strip()
            nuevo = Licoreria(codigo, nombre, marca, precio, stock, tipo_licor)

        elif categoria == "5":
            edad:   str = input("  Edad (ej: Cachorro, Adulto, Senior): ").strip()
            tamano: str = input("  Tamaño (ej: Pequeño, Mediano, Grande): ").strip()
            nuevo = Mascotas(codigo, nombre, marca, precio, stock, edad, tamano)
        
        elif categoria == "6":
            categoria_bebe: str = input("  Categoría (ej: Higiene, Nutrición, Ropa): ").strip()
            rango_edad:     str = input("  Rango de edad (ej: 0-6 meses): ").strip()
            nuevo = Bebes(codigo, nombre, marca, precio, stock, categoria_bebe, rango_edad)

        elif categoria == "7":
            categoria_hogar: str = input("  Categoría (ej: Decoración, Muebles): ").strip()
            habitacion:      str = input("  Habitación (ej: Sala, Cocina, Dormitorio): ").strip()
            nuevo = Hogar(codigo, nombre, marca, precio, stock, categoria_hogar, habitacion)

        elif categoria == "8":
            tipo:  str = input("  Tipo (ej: Camisa, Pantalón, Zapatos): ").strip()
            talla: str = input("  Talla (ej: S, M, L, XL): ").strip()
            color: str = input("  Color: ").strip()
            nuevo = Ropa(codigo, nombre, marca, precio, stock, tipo, talla, color)
            
        print(tienda.agregar_producto(nuevo))

    def editar_precio(self, tienda: Tienda, codigo: str, nuevo_precio: float) -> str:
        """Cambia el precio de un producto existente."""
        producto = tienda.buscar_por_codigo(codigo)
        if producto:
            return producto.cambiar_precio(nuevo_precio)
        else:
            return f"No se encontró el producto con código {codigo}."

    def actualizar_stock(self, tienda: Tienda, codigo: str, cantidad: int) -> str:
        """Agrega unidades al stock de un producto existente."""
        producto = tienda.buscar_por_codigo(codigo)
        if producto:
            return producto.agregar_stock(cantidad)
        else:
            return f"No se encontró el producto con código {codigo}."

    def eliminar_producto(self, tienda: Tienda, codigo: str) -> str:
        """Elimina un producto del catálogo."""
        return tienda.eliminar_producto(codigo)