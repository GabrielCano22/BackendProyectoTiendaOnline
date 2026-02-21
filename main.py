#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo principal: main.py
"""
from tienda import Tienda
from usuario import Cliente, Administrador
CLAVE_ADMIN = "admin123"
def menu_usuario(tienda, usuario):
    while True:
        print("\n" + "=" * 50)
        print(f"  BIENVENIDO, {usuario.nombre.upper()}")
        print("=" * 50)
        print("  1. Ver catálogo de productos")
        print("  2. Agregar producto al carrito")
        print("  3. Ver mi carrito")
        print("  4. Realizar compra")
        print("  5. Cerrar sesión")
        print("=" * 50)

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            tienda.mostrar_catalogo()

        elif opcion == "2":
            codigo = input("  Ingrese el código del producto: ").strip().upper()
            cantidad = input("  ¿Cuántas unidades desea agregar?: ").strip()
            if cantidad.isdigit() and int(cantidad) > 0:
                usuario.carrito.agregar_producto(tienda, codigo, int(cantidad))
            else:
                print("  Cantidad inválida.")

        elif opcion == "3":
            usuario.carrito.mostrar_carrito()

        elif opcion == "4":
            usuario.carrito.realizar_compra(tienda)

        elif opcion == "5":
            print(f"\n  Hasta pronto, {usuario.nombre}. ¡Gracias por visitarnos!")
            break

        else:
            print("  Opción no válida. Intente de nuevo.")

def menu_admin(tienda, admin):
    while True:
        print("\n" + "=" * 50)
        print(f"  PANEL ADMINISTRADOR - {admin.nombre.upper()}")
        print("=" * 50)
        print("  1. Ver catálogo completo")
        print("  2. Registrar nuevo producto")
        print("  3. Editar precio de un producto")
        print("  4. Actualizar stock de un producto")
        print("  5. Eliminar producto")
        print("  6. Cerrar sesión")
        print("=" * 50)

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            tienda.mostrar_catalogo()

        elif opcion == "2":
            admin.registrar_producto(tienda)

        elif opcion == "3":
            codigo = input("  Código del producto a editar: ").strip().upper()
            nuevo_precio = input("  Nuevo precio: ").strip()
            if nuevo_precio.replace(".", "", 1).isdigit():
                print(admin.editar_precio(tienda, codigo, float(nuevo_precio)))
            else:
                print("  Precio inválido.")

        elif opcion == "4":
            codigo = input("  Código del producto: ").strip().upper()
            cantidad = input("  Cantidad a agregar al stock: ").strip()
            if cantidad.isdigit() and int(cantidad) > 0:
                print(admin.actualizar_stock(tienda, codigo, int(cantidad)))
            else:
                print("  Cantidad inválida.")

        elif opcion == "5":
            codigo = input("  Código del producto a eliminar: ").strip().upper()
            confirmacion = (
                input(f"  ¿Seguro que desea eliminar {codigo}? (s/n): ").strip().lower()
            )
            if confirmacion == "s":
                print(admin.eliminar_producto(tienda, codigo))

        elif opcion == "6":
            print(f"\n  Sesión de administrador cerrada.")
            break

        else:
            print("  Opción no válida. Intente de nuevo.")
            
def menu_principal():
    print("\n" + "=" * 50)
    print("   TIENDA ONLINE - LA TIENDA DE GERARDO")
    print("=" * 50)
    print("  1. Ingresar como Usuario")
    print("  2. Ingresar como Administrador")
    print("  3. Salir")
    print("=" * 50)
    return input("  Seleccione una opción: ").strip()

def main():
    tienda = Tienda("La Tienda de Gerardo")
    tienda.cargar_productos_demo()  # Cambiar esto cuando ya tengamos todas las subclases establecidas

    print("\n  La Tienda de Gerardo.")

    while True:
        opcion = menu_principal()

        if opcion == "1":
            nombre = input("\n  Ingrese su nombre: ").strip()
            if nombre:
                usuario = Cliente(nombre)
                menu_usuario(tienda, usuario)
            else:
                print("  Nombre inválido.")

        elif opcion == "2":
            clave = input("\n  Ingrese la clave de administrador: ").strip()
            if clave == CLAVE_ADMIN:
                nombre = input("  Ingrese su nombre: ").strip()
                admin = Administrador(nombre)
                print(f"\n  Acceso concedido. Bienvenido, {admin.nombre}.")
                menu_admin(tienda, admin)
            else:
                print("\n  Clave incorrecta. Acceso denegado.")

        elif opcion == "3":
            print("\n  Gracias por usar el sistema. ¡Hasta pronto!\n")
            break

        else:
            print("  Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()