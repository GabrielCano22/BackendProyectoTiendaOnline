#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Sistema de gestión con ORM SQLAlchemy y Neon PostgreSQL
"""

from src.database.config import SessionLocal, create_tables
from src.entities.usuario import Usuario
from src.crud.usuario_crud import UsuarioCrud
from src.crud.categoria_crud import CategoriaCrud
from src.crud.producto_crud import ProductoCrud
from src.crud.tienda_crud import TiendaCrud
from src.crud.descuento_crud import DescuentoCrud
from src.crud.carrito_crud import CarritoCrud
from src.crud.factura_crud import FacturaCrud


class SistemaGestion:

    def __init__(self):
        self.db = SessionLocal()
        self.usuarioCrud = UsuarioCrud(self.db)
        self.categoriaCrud = CategoriaCrud(self.db)
        self.productoCrud = ProductoCrud(self.db)
        self.tiendaCrud = TiendaCrud(self.db)
        self.descuentoCrud = DescuentoCrud(self.db)
        self.carritoCrud = CarritoCrud(self.db)
        self.facturaCrud = FacturaCrud(self.db)
        self.usuario_actual = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def _setup_admin_inicial(self):
        """Si no existe ningún admin, pide crear el primero"""
        if not self.usuarioCrud.obtener_admin():
            print("\n" + "=" * 50)
            print("  PRIMER USO - CREAR ADMINISTRADOR")
            print("=" * 50)
            print("  No hay administrador registrado.")
            print("  Por favor crea el primer administrador.\n")
            while True:
                try:
                    nombre_completo = input("  Nombre completo: ").strip()
                    nombre_usuario = input("  Nombre de usuario: ").strip()
                    email = input("  Email: ").strip()
                    clave = input("  Clave: ").strip()
                    self.usuarioCrud.crear_usuario(
                        nombre_completo=nombre_completo,
                        nombre_usuario=nombre_usuario,
                        email=email,
                        clave=clave,
                        es_admin=True,
                    )
                    print(f"\n  Administrador '{nombre_completo}' creado exitosamente.")
                    break
                except ValueError as e:
                    print(f"\n  Error: {e}. Intente de nuevo.")

    def login(self) -> bool:
        print("\n" + "=" * 50)
        print("   TIENDA ONLINE - LA TIENDA DE GERARDO")
        print("=" * 50)

        while True:
            print("\n  1. Iniciar sesión")
            print("  2. Registrarse")
            print("  0. Salir")
            opcion = input("\n  Seleccione una opción: ").strip()

            if opcion == "1":
                for intento in range(1, 4):
                    print(f"\n  Intento {intento} de 3")
                    usuario_input = input("  Usuario o email: ").strip()
                    clave = input("  Clave: ").strip()
                    usuario = self.usuarioCrud.autenticar_usuario(usuario_input, clave)
                    if usuario:
                        self.usuario_actual = usuario
                        rol = "Administrador" if usuario.es_admin else "Cliente"
                        print(f"\n  Bienvenido, {usuario.nombre_completo} ({rol})")
                        return True
                    print("  Usuario o clave incorrectos.")
                print("\n  Demasiados intentos fallidos.")
                return False

            elif opcion == "2":
                self._registrar_cliente()

            elif opcion == "0":
                return False

            else:
                print("  Opción no válida.")

    def _registrar_cliente(self):
        print("\n" + "-" * 40)
        print("  REGISTRO DE CLIENTE")
        print("-" * 40)
        try:
            nombre_completo = input("  Nombre completo: ").strip()
            nombre_usuario = input("  Nombre de usuario: ").strip()
            email = input("  Email: ").strip()
            telefono = input("  Teléfono (opcional): ").strip() or None
            clave = input("  Clave: ").strip()
            nuevo = self.usuarioCrud.crear_usuario(
                nombre_completo=nombre_completo,
                nombre_usuario=nombre_usuario,
                email=email,
                clave=clave,
                telefono=telefono,
                es_admin=False,
            )
            print(f"\n  Cliente '{nuevo.nombre_completo}' registrado exitosamente.")
            print("  Ya puedes iniciar sesión.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def menu_principal(self):
        while True:
            print("\n" + "=" * 50)
            print(f"  MENÚ PRINCIPAL - {self.usuario_actual.nombre_completo.upper()}")
            print("=" * 50)
            if self.usuario_actual.es_admin:
                print("  1. Gestión de Usuarios")
                print("  2. Gestión de Categorías")
                print("  3. Gestión de Productos")
                print("  4. Gestión de Facturas")
            else:
                print("  1. Ver catálogo")
                print("  2. Buscar producto por nombre")
                print("  3. Buscar producto por categoría")
                print("  4. Mi carrito")
                print("  5. Mis facturas")
                print("  0. Cerrar sesión")
                print("=" * 50)

            opcion = input("  Seleccione una opción: ").strip()

            if self.usuario_actual.es_admin:
                if opcion == "1":
                    self.menu_usuarios()
                elif opcion == "2":
                    self.menu_categorias()
                elif opcion == "3":
                    self.menu_productos()
                elif opcion == "4":
                    self.menu_facturas()
                elif opcion == "0":
                    print(f"\n  Hasta pronto, {self.usuario_actual.nombre_completo}!")
                    break
                else:
                    print("  Opción no válida.")
            else:
                if opcion == "1":
                    self._ver_catalogo()
                elif opcion == "2":
                    self._buscar_por_nombre()
                elif opcion == "3":
                    self._buscar_por_categoria()
                elif opcion == "4":
                    self.menu_carrito()
                elif opcion == "5":
                    self.menu_facturas()
                elif opcion == "0":
                    print(f"\n  Hasta pronto, {self.usuario_actual.nombre_completo}!")
                    break
                else:
                    print("  Opción no válida.")

    def menu_usuarios(self):
        while True:
            print("\n" + "-" * 40)
            print("  GESTIÓN DE USUARIOS")
            print("-" * 40)
            print("  1. Listar usuarios")
            print("  2. Crear administrador")
            print("  3. Eliminar usuario")
            print("  0. Volver")
            opcion = input("  Seleccione una opción: ").strip()

            if opcion == "1":
                self._listar_usuarios()
            elif opcion == "2":
                self._crear_admin()
            elif opcion == "3":
                self._eliminar_usuario()
            elif opcion == "0":
                break
            else:
                print("  Opción no válida.")

    def _listar_usuarios(self):
        usuarios = self.usuarioCrud.obtener_usuarios()
        if not usuarios:
            print("\n  No hay usuarios registrados.")
            return
        print(f"\n  Total: {len(usuarios)} usuarios")
        print(f"  {'NOMBRE':<25} {'USUARIO':<20} {'EMAIL':<30} {'ROL':<10}")
        print(f"  {'-' * 85}")
        for u in usuarios:
            rol = "ADMIN" if u.es_admin else "cliente"
            print(
                f"  {u.nombre_completo:<25} {u.nombre_usuario:<20} {u.email:<30} {rol:<10}"
            )

    def _crear_admin(self):
        print("\n" + "-" * 40)
        print("  CREAR ADMINISTRADOR")
        print("-" * 40)
        try:
            nombre_completo = input("  Nombre completo: ").strip()
            nombre_usuario = input("  Nombre de usuario: ").strip()
            email = input("  Email: ").strip()
            clave = input("  Clave: ").strip()
            nuevo = self.usuarioCrud.crear_usuario(
                nombre_completo=nombre_completo,
                nombre_usuario=nombre_usuario,
                email=email,
                clave=clave,
                es_admin=True,
            )
            print(f"\n  Administrador '{nuevo.nombre_completo}' creado exitosamente.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _eliminar_usuario(self):
        self._listar_usuarios()
        usuario_input = input("\n  Nombre de usuario a eliminar: ").strip()
        usuario = (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == usuario_input)
            .first()
        )
        if not usuario:
            print("  Usuario no encontrado.")
            return
        confirmar = (
            input(f"  ¿Eliminar '{usuario.nombre_completo}'? (s/n): ").strip().lower()
        )
        if confirmar == "s":
            self.usuarioCrud.eliminar_usuario(usuario.id_usuario)
            print(f"  Usuario '{usuario.nombre_completo}' eliminado.")

    def menu_categorias(self):
        while True:
            print("\n" + "-" * 40)
            print("  GESTIÓN DE CATEGORÍAS")
            print("-" * 40)
            print("  1. Listar categorías")
            print("  2. Crear categoría")
            print("  3. Actualizar categoría")
            print("  4. Eliminar categoría")
            print("  0. Volver")
            opcion = input("  Seleccione una opción: ").strip()

            if opcion == "1":
                self._listar_categorias()
            elif opcion == "2":
                self._crear_categoria()
            elif opcion == "3":
                self._actualizar_categoria()
            elif opcion == "4":
                self._eliminar_categoria()
            elif opcion == "0":
                break
            else:
                print("  Opción no válida.")

    def _listar_categorias(self):
        categorias = self.categoriaCrud.obtener_categorias()
        if not categorias:
            print("\n  No hay categorías registradas.")
            return
        print(f"\n  Total: {len(categorias)} categorías")
        print(f"  {'NOMBRE':<25} {'DESCRIPCIÓN':<40}")
        print(f"  {'-' * 65}")
        for c in categorias:
            desc = c.descripcion or "Sin descripción"
            print(f"  {c.nombre:<25} {desc:<40}")

    def _crear_categoria(self):
        try:
            nombre = input("  Nombre de la categoría: ").strip()
            descripcion = input("  Descripción (opcional): ").strip() or None
            nueva = self.categoriaCrud.crear_categoria(
                nombre=nombre,
                descripcion=descripcion,
                usuario_id=self.usuario_actual.id_usuario,
            )
            print(f"\n  Categoría '{nueva.nombre}' creada exitosamente.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _actualizar_categoria(self):
        self._listar_categorias()
        nombre = input("\n  Nombre de la categoría a actualizar: ").strip()
        categoria = self.categoriaCrud.obtener_categoria_por_nombre(nombre)
        if not categoria:
            print("  Categoría no encontrada.")
            return
        try:
            nuevo_nombre = input(f"  Nuevo nombre ({categoria.nombre}): ").strip()
            nueva_desc = input(
                f"  Nueva descripción ({categoria.descripcion}): "
            ).strip()
            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nueva_desc:
                cambios["descripcion"] = nueva_desc
            if cambios:
                self.categoriaCrud.actualizar_categoria(
                    categoria.id_categoria,
                    self.usuario_actual.id_usuario,
                    **cambios,
                )
                print("  Categoría actualizada exitosamente.")
            else:
                print("  No se realizaron cambios.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _eliminar_categoria(self):
        self._listar_categorias()
        nombre = input("\n  Nombre de la categoría a eliminar: ").strip()
        categoria = self.categoriaCrud.obtener_categoria_por_nombre(nombre)
        if not categoria:
            print("  Categoría no encontrada.")
            return
        confirmar = input(f"  ¿Eliminar '{categoria.nombre}'? (s/n): ").strip().lower()
        if confirmar == "s":
            self.categoriaCrud.eliminar_categoria(categoria.id_categoria)
            print(f"  Categoría '{categoria.nombre}' eliminada.")

    def menu_productos(self):
        while True:
            print("\n" + "-" * 40)
            print("  GESTIÓN DE PRODUCTOS")
            print("-" * 40)
            print("  1. Ver catálogo")
            print("  2. Buscar por código")
            print("  3. Buscar por nombre")
            print("  4. Buscar por categoría")
            print("  5. Crear producto")
            print("  6. Actualizar producto")
            print("  7. Eliminar producto")
            print("  0. Volver")
            opcion = input("  Seleccione una opción: ").strip()

            if opcion == "1":
                self._ver_catalogo()
            elif opcion == "2":
                self._buscar_por_codigo()
            elif opcion == "3":
                self._buscar_por_nombre()
            elif opcion == "4":
                self._buscar_por_categoria()
            elif opcion == "5":
                self._crear_producto()
            elif opcion == "6":
                self._actualizar_producto()
            elif opcion == "7":
                self._eliminar_producto()
            elif opcion == "0":
                break
            else:
                print("  Opción no válida.")

    def _ver_catalogo(self):
        productos = self.productoCrud.obtener_productos()
        if not productos:
            print("\n  El catálogo está vacío.")
            return
        print(f"\n{'=' * 75}")
        print(f"  CATÁLOGO - LA TIENDA DE GERARDO  ({len(productos)} productos)")
        print(f"{'=' * 75}")
        print(
            f"  {'CÓDIGO':<12} {'NOMBRE':<25} {'MARCA':<12} {'PRECIO':>12} {'STOCK':>6}"
        )
        print(f"  {'-' * 70}")
        for p in productos:
            print(
                f"  {p.codigo:<12} {p.nombre:<25} {p.marca:<12} "
                f"${float(p.precio):>10,.0f} {p.stock:>6}"
            )
        print(f"{'=' * 75}")

    def _buscar_por_codigo(self):
        codigo = input("  Código del producto: ").strip().upper()
        producto = self.productoCrud.obtener_producto_por_codigo(codigo)
        if producto:
            print(
                f"\n  [{producto.codigo}] {producto.nombre} | "
                f"{producto.marca} | ${float(producto.precio):,.0f} | "
                f"Stock: {producto.stock}"
            )
        else:
            print(f"  No se encontró el producto '{codigo}'.")

    def _buscar_por_nombre(self):
        nombre = input("  Nombre a buscar: ").strip()
        productos = self.productoCrud.buscar_productos_por_nombre(nombre)
        if productos:
            for p in productos:
                print(
                    f"  [{p.codigo}] {p.nombre} | {p.marca} | "
                    f"${float(p.precio):,.0f} | Stock: {p.stock}"
                )
        else:
            print(f"  No se encontraron productos con '{nombre}'.")

    def _buscar_por_categoria(self):
        self._listar_categorias()
        nombre = input("\n  Nombre de la categoría: ").strip()
        categoria = self.categoriaCrud.obtener_categoria_por_nombre(nombre)
        if not categoria:
            print("  Categoría no encontrada.")
            return
        productos = self.productoCrud.obtener_productos_por_categoria(
            categoria.id_categoria
        )
        if productos:
            for p in productos:
                print(
                    f"  [{p.codigo}] {p.nombre} | {p.marca} | "
                    f"${float(p.precio):,.0f} | Stock: {p.stock}"
                )
        else:
            print(f"  No hay productos en la categoría '{nombre}'.")

    def _crear_producto(self):
        self._listar_categorias()
        try:
            nombre = input("\n  Nombre del producto: ").strip()
            tipo_producto = input("  Tipo de producto: ").strip()
            codigo = input("  Código (ej: ALI-001): ").strip().upper()
            marca = input("  Marca: ").strip()
            precio = float(input("  Precio (COP): ").strip())
            stock = int(input("  Stock inicial: ").strip())
            descripcion = input("  Descripción (opcional): ").strip() or None
            nombre_categoria = input("  Nombre de la categoría: ").strip()
            categoria = self.categoriaCrud.obtener_categoria_por_nombre(
                nombre_categoria
            )
            if not categoria:
                print("  Categoría no encontrada.")
                return
            nuevo = self.productoCrud.crear_producto(
                nombre=nombre,
                tipo_producto=tipo_producto,
                codigo=codigo,
                marca=marca,
                precio=precio,
                stock=stock,
                descripcion=descripcion,
                categoria_id=categoria.id_categoria,
                usuario_id=self.usuario_actual.id_usuario,
            )
            print(f"\n  Producto '{nuevo.nombre}' creado exitosamente.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _actualizar_producto(self):
        codigo = input("  Código del producto a actualizar: ").strip().upper()
        producto = self.productoCrud.obtener_producto_por_codigo(codigo)
        if not producto:
            print("  Producto no encontrado.")
            return
        try:
            nuevo_nombre = input(f"  Nuevo nombre ({producto.nombre}): ").strip()
            nuevo_precio = input(f"  Nuevo precio ({producto.precio}): ").strip()
            nuevo_stock = input(f"  Nuevo stock ({producto.stock}): ").strip()
            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_precio:
                cambios["precio"] = float(nuevo_precio)
            if nuevo_stock:
                cambios["stock"] = int(nuevo_stock)
            if cambios:
                self.productoCrud.actualizar_producto(
                    producto.id_producto,
                    self.usuario_actual.id_usuario,
                    **cambios,
                )
                print("  Producto actualizado exitosamente.")
            else:
                print("  No se realizaron cambios.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _eliminar_producto(self):
        codigo = input("  Código del producto a eliminar: ").strip().upper()
        producto = self.productoCrud.obtener_producto_por_codigo(codigo)
        if not producto:
            print("  Producto no encontrado.")
            return
        confirmar = input(f"  ¿Eliminar '{producto.nombre}'? (s/n): ").strip().lower()
        if confirmar == "s":
            self.productoCrud.eliminar_producto(
                producto.id_producto,
                self.usuario_actual.id_usuario,
            )
            print(f"  Producto '{producto.nombre}' eliminado.")

    def menu_carrito(self):
        while True:
            print("\n" + "-" * 40)
            print("  MI CARRITO")
            print("-" * 40)
            print("  1. Ver carrito actual")
            print("  2. Agregar producto")
            print("  3. Cambiar cantidad")
            print("  4. Eliminar producto")
            print("  5. Vaciar carrito")
            print("  6. Generar factura")
            print("  0. Volver")
            opcion = input("  Seleccione una opción: ").strip()

            if opcion == "1":
                self._ver_carrito()
            elif opcion == "2":
                self._agregar_al_carrito()
            elif opcion == "3":
                self._cambiar_cantidad()
            elif opcion == "4":
                self._eliminar_del_carrito()
            elif opcion == "5":
                self._vaciar_carrito()
            elif opcion == "6":
                self._generar_factura()
            elif opcion == "0":
                break
            else:
                print("  Opción no válida.")

    def _obtener_o_crear_carrito(self):
        """Retorna el carrito activo del usuario, o crea uno nuevo si no existe."""
        carrito = self.carritoCrud.obtener_carrito_activo(
            self.usuario_actual.id_usuario
        )
        if not carrito:
            carrito = self.carritoCrud.crear_carrito(self.usuario_actual.id_usuario)
        return carrito

    def _ver_carrito(self):
        carrito = self.carritoCrud.obtener_carrito_activo(
            self.usuario_actual.id_usuario
        )
        if not carrito:
            print("\n  Tu carrito está vacío.")
            return
        detalles = self.carritoCrud.obtener_detalles(carrito.id_carrito)
        if not detalles:
            print("\n  Tu carrito está vacío.")
            return
        print(f"\n{'=' * 65}")
        print(f"  CARRITO  (estado: {carrito.estado})")
        print(f"{'=' * 65}")
        print(
            f"  {'CÓDIGO':<12} {'PRODUCTO':<25} {'PRECIO UNIT':>12} {'CANT':>6} {'SUBTOTAL':>12}"
        )
        print(f"  {'-' * 60}")
        for d in detalles:
            subtotal = float(d.precio_unitario) * d.cantidad
            print(
                f"  {d.producto.codigo:<12} {d.producto.nombre:<25} "
                f"${float(d.precio_unitario):>10,.0f} "
                f"{d.cantidad:>6} "
                f"${subtotal:>10,.0f}"
            )
        total = self.carritoCrud.calcular_total(carrito.id_carrito)
        unidades = self.carritoCrud.contar_unidades(carrito.id_carrito)
        descuento = self.descuentoCrud.aplicar_descuento(unidades)
        print(f"  {'-' * 60}")
        print(f"  Total unidades: {unidades}  |  Descuento aplicable: {descuento}%")
        print(f"  TOTAL BRUTO: ${float(total):>10,.0f}")
        print(f"{'=' * 65}")

    def _agregar_al_carrito(self):
        self._ver_catalogo()
        try:
            codigo = input("\n  Código del producto: ").strip().upper()
            producto = self.productoCrud.obtener_producto_por_codigo(codigo)
            if not producto:
                print("  Producto no encontrado.")
                return
            cantidad = int(
                input(f"  Cantidad (stock disponible: {producto.stock}): ").strip()
            )
            carrito = self._obtener_o_crear_carrito()
            self.carritoCrud.agregar_producto(
                carrito.id_carrito, producto.id_producto, cantidad
            )
            print(f"\n  '{producto.nombre}' x{cantidad} agregado al carrito.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _cambiar_cantidad(self):
        self._ver_carrito()
        carrito = self.carritoCrud.obtener_carrito_activo(
            self.usuario_actual.id_usuario
        )
        if not carrito:
            return
        try:
            codigo = input("\n  Código del producto a modificar: ").strip().upper()
            producto = self.productoCrud.obtener_producto_por_codigo(codigo)
            if not producto:
                print("  Producto no encontrado.")
                return
            nueva_cantidad = int(input("  Nueva cantidad (0 para eliminar): ").strip())
            self.carritoCrud.actualizar_cantidad(
                carrito.id_carrito, producto.id_producto, nueva_cantidad
            )
            if nueva_cantidad == 0:
                print("  Producto eliminado del carrito.")
            else:
                print(f"  Cantidad actualizada a {nueva_cantidad}.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _eliminar_del_carrito(self):
        self._ver_carrito()
        carrito = self.carritoCrud.obtener_carrito_activo(
            self.usuario_actual.id_usuario
        )
        if not carrito:
            return
        codigo = input("\n  Código del producto a eliminar: ").strip().upper()
        producto = self.productoCrud.obtener_producto_por_codigo(codigo)
        if not producto:
            print("  Producto no encontrado.")
            return
        eliminado = self.carritoCrud.eliminar_producto(
            carrito.id_carrito, producto.id_producto
        )
        if eliminado:
            print(f"  '{producto.nombre}' eliminado del carrito.")
        else:
            print("  El producto no estaba en el carrito.")

    def _vaciar_carrito(self):
        carrito = self.carritoCrud.obtener_carrito_activo(
            self.usuario_actual.id_usuario
        )
        if not carrito:
            print("  No tienes un carrito activo.")
            return
        confirmar = input("  ¿Vaciar todo el carrito? (s/n): ").strip().lower()
        if confirmar == "s":
            self.carritoCrud.vaciar_carrito(carrito.id_carrito)
            print("  Carrito vaciado.")

    def _generar_factura(self):
        self._ver_carrito()
        carrito = self.carritoCrud.obtener_carrito_activo(
            self.usuario_actual.id_usuario
        )
        if not carrito:
            print("  No tienes un carrito activo.")
            return
        confirmar = (
            input("\n  ¿Confirmar compra y generar factura? (s/n): ").strip().lower()
        )
        if confirmar == "s":
            try:
                factura = self.facturaCrud.generar_factura(
                    carrito.id_carrito,
                    self.usuario_actual.id_usuario,
                )
                print(f"\n{'=' * 50}")
                print("  ¡FACTURA GENERADA EXITOSAMENTE!")
                print(f"{'=' * 50}")
                print(f"  ID Factura   : {str(factura.id_factura)[:8]}...")
                print(f"  Total bruto  : ${float(factura.total_bruto):>10,.0f}")
                print(
                    f"  Descuento    : {float(factura.porcentaje_descuento)}%  -${float(factura.total_descuento):>8,.0f}"
                )
                print(f"  TOTAL A PAGAR: ${float(factura.total_neto):>10,.0f}")
                print(f"{'=' * 50}")
            except ValueError as e:
                print(f"\n  Error: {e}")

    # ------------------------------------------------------------------ #
    #  Menú de Facturas                                                    #
    # ------------------------------------------------------------------ #

    def menu_facturas(self):
        while True:
            print("\n" + "-" * 40)
            print("  MIS FACTURAS")
            print("-" * 40)
            print("  1. Ver mis facturas")
            print("  2. Ver detalle de una factura")
            if self.usuario_actual.es_admin:
                print("  3. Ver todas las facturas")
                print("  4. Marcar factura como pagada")
                print("  5. Anular factura")
            print("  0. Volver")
            opcion = input("  Seleccione una opción: ").strip()

            if opcion == "1":
                self._listar_mis_facturas()
            elif opcion == "2":
                self._ver_detalle_factura()
            elif opcion == "3" and self.usuario_actual.es_admin:
                self._listar_todas_las_facturas()
            elif opcion == "4" and self.usuario_actual.es_admin:
                self._marcar_pagada()
            elif opcion == "5" and self.usuario_actual.es_admin:
                self._anular_factura()
            elif opcion == "0":
                break
            else:
                print("  Opción no válida.")

    def _listar_mis_facturas(self):
        facturas = self.facturaCrud.obtener_facturas_por_usuario(
            self.usuario_actual.id_usuario
        )
        self._imprimir_facturas(facturas)

    def _listar_todas_las_facturas(self):
        facturas = self.facturaCrud.obtener_todas_las_facturas()
        self._imprimir_facturas(facturas)

    def _imprimir_facturas(self, facturas):
        if not facturas:
            print("\n  No hay facturas registradas.")
            return
        print(
            f"\n  {'ID':<12} {'TOTAL NETO':>12} {'DESCUENTO':>10} {'ESTADO':<12} {'FECHA'}"
        )
        print(f"  {'-' * 65}")
        for f in facturas:
            fecha = (
                f.fecha_creacion.strftime("%Y-%m-%d %H:%M") if f.fecha_creacion else "-"
            )
            print(
                f"  {str(f.id_factura)[:8]+'...':<12} "
                f"${float(f.total_neto):>10,.0f} "
                f"{float(f.porcentaje_descuento):>9.0f}% "
                f"{f.estado:<12} "
                f"{fecha}"
            )

    def _ver_detalle_factura(self):
        self._listar_mis_facturas()
        id_input = input("\n  Primeros 8 caracteres del ID de la factura: ").strip()
        facturas = self.facturaCrud.obtener_facturas_por_usuario(
            self.usuario_actual.id_usuario
        )
        factura = next(
            (f for f in facturas if str(f.id_factura).startswith(id_input)), None
        )
        if not factura:
            print("  Factura no encontrada.")
            return
        detalles = self.facturaCrud.obtener_detalles_por_factura(factura.id_factura)
        print(f"\n{'=' * 60}")
        print(f"  DETALLE FACTURA  (estado: {factura.estado})")
        print(f"{'=' * 60}")
        print(f"  {'PRODUCTO':<25} {'P.UNIT':>12} {'CANT':>6} {'SUBTOTAL':>12}")
        print(f"  {'-' * 58}")
        for d in detalles:
            print(
                f"  {d.nombre_producto:<25} "
                f"${float(d.precio_unitario):>10,.0f} "
                f"{d.cantidad:>6} "
                f"${float(d.subtotal):>10,.0f}"
            )
        print(f"  {'-' * 58}")
        print(f"  Total bruto  : ${float(factura.total_bruto):>10,.0f}")
        print(
            f"  Descuento    : {float(factura.porcentaje_descuento):.0f}%  -${float(factura.total_descuento):>8,.0f}"
        )
        print(f"  TOTAL NETO   : ${float(factura.total_neto):>10,.0f}")
        print(f"{'=' * 60}")

    def _marcar_pagada(self):
        self._listar_todas_las_facturas()
        id_input = input("\n  Primeros 8 caracteres del ID: ").strip()
        facturas = self.facturaCrud.obtener_todas_las_facturas()
        factura = next(
            (f for f in facturas if str(f.id_factura).startswith(id_input)), None
        )
        if not factura:
            print("  Factura no encontrada.")
            return
        try:
            self.facturaCrud.marcar_como_pagada(factura.id_factura)
            print("  Factura marcada como pagada.")
        except ValueError as e:
            print(f"\n  Error: {e}")

    def _anular_factura(self):
        self._listar_todas_las_facturas()
        id_input = input("\n  Primeros 8 caracteres del ID: ").strip()
        facturas = self.facturaCrud.obtener_todas_las_facturas()
        factura = next(
            (f for f in facturas if str(f.id_factura).startswith(id_input)), None
        )
        if not factura:
            print("  Factura no encontrada.")
            return
        confirmar = (
            input(f"  ¿Anular factura y devolver stock? (s/n): ").strip().lower()
        )
        if confirmar == "s":
            try:
                self.facturaCrud.anular_factura(factura.id_factura)
                print("  Factura anulada y stock devuelto.")
            except ValueError as e:
                print(f"\n  Error: {e}")

    def ejecutar(self):
        try:
            print("\n  Iniciando La Tienda de Gerardo...")
            print("  Conectando a la base de datos Neon...")
            create_tables()
            print("  Base de datos lista.")
            self.tiendaCrud.inicializar()
            self.descuentoCrud.seed_descuentos_base()
            self._setup_admin_inicial()

            if not self.login():
                print("\n  Saliendo del sistema. ¡Hasta luego!")
                return

            self.menu_principal()

        except KeyboardInterrupt:
            print("\n\n  Sistema interrumpido.")
        except Exception as e:
            print(f"\n  Error crítico: {e}")
        finally:
            self.db.close()
