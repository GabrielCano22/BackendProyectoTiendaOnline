#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: src/crud/carrito_crud.py
"""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, selectinload
from src.entities.carrito import Carrito
from src.entities.detalle_carrito import DetalleCarrito
from src.entities.producto import Producto

class CarritoCrud:
    def __init__(self, db: Session):
        self.db = db

    def crear_carrito(self, usuario_id: UUID) -> Carrito:
        """Crea un carrito nuevo en estado 'activo' para el usuario."""
        carrito = Carrito(
            id_usuario=usuario_id,
            estado="activo",
        )
        self.db.add(carrito)
        self.db.commit()
        self.db.refresh(carrito)
        return carrito

    def obtener_carrito_por_id(self, carrito_id: UUID) -> Optional[Carrito]:
        """Busca un carrito por su UUID."""
        return self.db.query(Carrito).filter(Carrito.id_carrito == carrito_id).first()

    def obtener_carrito_activo(self, usuario_id: UUID) -> Optional[Carrito]:
        """Retorna el carrito activo del usuario, si existe."""
        return (
            self.db.query(Carrito)
            .options(
                selectinload(Carrito.detalles).selectinload(DetalleCarrito.producto)
            )
            .filter(
                Carrito.id_usuario == usuario_id,
                Carrito.estado == "activo",
            )
            .first()
        )

    def obtener_carritos_por_usuario(self, usuario_id: UUID) -> List[Carrito]:
        """Lista todos los carritos (de cualquier estado) de un usuario."""
        return self.db.query(Carrito).filter(Carrito.id_usuario == usuario_id).all()

    def finalizar_carrito(self, carrito_id: UUID) -> Optional[Carrito]:
        """Cambia el estado del carrito a 'finalizado' (cuando se genera la factura)."""
        carrito = self.obtener_carrito_por_id(carrito_id)
        if not carrito:
            return None
        carrito.estado = "finalizado"
        self.db.commit()
        self.db.refresh(carrito)
        return carrito

    def cancelar_carrito(self, carrito_id: UUID) -> Optional[Carrito]:
        """Cambia el estado del carrito a 'cancelado'."""
        carrito = self.obtener_carrito_por_id(carrito_id)
        if not carrito:
            return None
        carrito.estado = "cancelado"
        self.db.commit()
        self.db.refresh(carrito)
        return carrito

    def agregar_producto(
        self, carrito_id: UUID, producto_id: UUID, cantidad: int
    ) -> DetalleCarrito:
        """
        Agrega un producto al carrito.
        - Valida que el carrito esté activo.
        - Valida que haya stock suficiente.
        - Si el producto ya estaba en el carrito, suma la cantidad.
        """
        if cantidad < 1:
            raise ValueError("La cantidad debe ser al menos 1")

        carrito = self.obtener_carrito_por_id(carrito_id)
        if not carrito:
            raise ValueError("El carrito no existe")
        if carrito.estado != "activo":
            raise ValueError("Solo se pueden modificar carritos activos")

        producto = (
            self.db.query(Producto)
            .filter(Producto.id_producto == producto_id, Producto.eliminado == False)
            .first()
        )
        if not producto:
            raise ValueError("El producto no existe o fue eliminado")
        if producto.stock < cantidad:
            raise ValueError(
                f"Stock insuficiente. Disponible: {producto.stock}, solicitado: {cantidad}"
            )

        detalle = (
            self.db.query(DetalleCarrito)
            .filter(
                DetalleCarrito.id_carrito == carrito_id,
                DetalleCarrito.id_producto == producto_id,
            )
            .first()
        )

        if detalle:
            nueva_cantidad = detalle.cantidad + cantidad
            if producto.stock < nueva_cantidad:
                raise ValueError(
                    f"Stock insuficiente. Disponible: {producto.stock}, total solicitado: {nueva_cantidad}"
                )
            detalle.cantidad = nueva_cantidad
        else:
            detalle = DetalleCarrito(
                id_carrito=carrito_id,
                id_producto=producto_id,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )
            self.db.add(detalle)

        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_detalles(self, carrito_id: UUID) -> List[DetalleCarrito]:
        """Lista todos los productos dentro de un carrito."""
        return (
            self.db.query(DetalleCarrito)
            .filter(DetalleCarrito.id_carrito == carrito_id)
            .all()
        )

    def actualizar_cantidad(
        self, carrito_id: UUID, producto_id: UUID, nueva_cantidad: int
    ) -> Optional[DetalleCarrito]:
        """
        Cambia la cantidad de un producto en el carrito.
        Si nueva_cantidad es 0, elimina el detalle.
        """
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        detalle = (
            self.db.query(DetalleCarrito)
            .filter(
                DetalleCarrito.id_carrito == carrito_id,
                DetalleCarrito.id_producto == producto_id,
            )
            .first()
        )
        if not detalle:
            return None

        if nueva_cantidad == 0:
            self.db.delete(detalle)
            self.db.commit()
            return None

        producto = (
            self.db.query(Producto).filter(Producto.id_producto == producto_id).first()
        )
        if producto and producto.stock < nueva_cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")

        detalle.cantidad = nueva_cantidad
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def eliminar_producto(self, carrito_id: UUID, producto_id: UUID) -> bool:
        """Elimina un producto del carrito."""
        detalle = (
            self.db.query(DetalleCarrito)
            .filter(
                DetalleCarrito.id_carrito == carrito_id,
                DetalleCarrito.id_producto == producto_id,
            )
            .first()
        )
        if not detalle:
            return False

        self.db.delete(detalle)
        self.db.commit()
        return True

    def vaciar_carrito(self, carrito_id: UUID) -> bool:
        """Elimina todos los productos de un carrito."""
        carrito = self.obtener_carrito_por_id(carrito_id)
        if not carrito:
            return False

        self.db.query(DetalleCarrito).filter(
            DetalleCarrito.id_carrito == carrito_id
        ).delete()
        self.db.commit()
        return True

    def calcular_total(self, carrito_id: UUID) -> Decimal:
        """Retorna el total bruto del carrito (sin descuentos)."""
        detalles = self.obtener_detalles(carrito_id)
        return sum(Decimal(str(d.precio_unitario)) * d.cantidad for d in detalles)

    def contar_unidades(self, carrito_id: UUID) -> int:
        """Retorna el total de unidades en el carrito (para calcular descuentos)."""
        detalles = self.obtener_detalles(carrito_id)
        return sum(d.cantidad for d in detalles)