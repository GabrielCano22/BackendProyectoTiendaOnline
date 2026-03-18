#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
Archivo: src/crud/factura_crud.py
"""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.factura import Factura
from src.entities.detalle_factura import DetalleFactura
from src.entities.carrito import Carrito
from src.entities.detalle_carrito import DetalleCarrito
from src.entities.producto import Producto
from src.crud.carrito_crud import CarritoCrud
from src.crud.descuento_crud import DescuentoCrud


class FacturaCrud:
    def __init__(self, db: Session):
        self.db = db

    def generar_factura(self, carrito_id: UUID, usuario_id: UUID) -> Factura:
        """
        Genera una factura a partir de un carrito activo.
        - Aplica descuentos según las reglas del DescuentoCrud.
        - Descuenta el stock de cada producto.
        - Finaliza el carrito.
        """
        carrito_crud = CarritoCrud(self.db)
        descuento_crud = DescuentoCrud(self.db)

        carrito = carrito_crud.obtener_carrito_por_id(carrito_id)
        if not carrito:
            raise ValueError("El carrito no existe")
        if carrito.estado != "activo":
            raise ValueError("Solo se puede facturar un carrito activo")
        if carrito.id_usuario != usuario_id:
            raise ValueError("El carrito no pertenece al usuario indicado")

        detalles_carrito = carrito_crud.obtener_detalles(carrito_id)
        if not detalles_carrito:
            raise ValueError("No se puede facturar un carrito vacío")

        for detalle in detalles_carrito:
            producto = (
                self.db.query(Producto)
                .filter(Producto.id_producto == detalle.id_producto)
                .first()
            )
            if not producto or producto.eliminado:
                raise ValueError(
                    f"El producto con id '{detalle.id_producto}' ya no está disponible"
                )
            if producto.stock < detalle.cantidad:
                raise ValueError(
                    f"Stock insuficiente para '{producto.nombre}'. "
                    f"Disponible: {producto.stock}, solicitado: {detalle.cantidad}"
                )

        total_unidades = carrito_crud.contar_unidades(carrito_id)
        total_bruto = carrito_crud.calcular_total(carrito_id)
        porcentaje_descuento = descuento_crud.aplicar_descuento(total_unidades)
        total_descuento = (
            total_bruto * porcentaje_descuento / Decimal("100")
        ).quantize(Decimal("0.01"))
        total_neto = total_bruto - total_descuento

        factura = Factura(
            id_usuario=usuario_id,
            id_carrito=carrito_id,
            total_bruto=total_bruto,
            porcentaje_descuento=porcentaje_descuento,
            total_descuento=total_descuento,
            total_neto=total_neto,
            estado="Pagada",
        )
        self.db.add(factura)
        self.db.flush()

        for detalle in detalles_carrito:
            producto = (
                self.db.query(Producto)
                .filter(Producto.id_producto == detalle.id_producto)
                .first()
            )
            subtotal = (
                Decimal(str(detalle.precio_unitario)) * detalle.cantidad
            ).quantize(Decimal("0.01"))

            detalle_factura = DetalleFactura(
                id_factura=factura.id_factura,
                id_producto=detalle.id_producto,
                nombre_producto=producto.nombre,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=subtotal,
            )
            self.db.add(detalle_factura)

            producto.stock -= detalle.cantidad

        carrito_crud.finalizar_carrito(carrito_id)

        self.db.commit()
        self.db.refresh(factura)
        return factura

    def obtener_factura_por_id(self, factura_id: UUID) -> Optional[Factura]:
        """Busca una factura por su UUID."""
        return self.db.query(Factura).filter(Factura.id_factura == factura_id).first()

    def obtener_facturas_por_usuario(self, usuario_id: UUID) -> List[Factura]:
        """Lista todas las facturas de un usuario."""
        return self.db.query(Factura).filter(Factura.id_usuario == usuario_id).all()

    def obtener_todas_las_facturas(self) -> List[Factura]:
        """Lista todas las facturas del sistema (solo para admins)."""
        return self.db.query(Factura).all()

    def marcar_como_pagada(self, factura_id: UUID) -> Optional[Factura]:
        """Cambia el estado de la factura a 'pagada'."""
        factura = self.obtener_factura_por_id(factura_id)
        if not factura:
            return None
        if factura.estado != "pendiente":
            raise ValueError("Solo se pueden pagar facturas en estado 'pendiente'")
        factura.estado = "pagada"
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def anular_factura(self, factura_id: UUID) -> Optional[Factura]:
        """
        Anula una factura y devuelve el stock de los productos.
        Solo se puede anular si está en estado 'pendiente'.
        """
        factura = self.obtener_factura_por_id(factura_id)
        if not factura:
            return None
        if factura.estado != "pendiente":
            raise ValueError("Solo se pueden anular facturas en estado 'pendiente'")

        detalles = self.obtener_detalles_por_factura(factura_id)
        for detalle in detalles:
            producto = (
                self.db.query(Producto)
                .filter(Producto.id_producto == detalle.id_producto)
                .first()
            )
            if producto:
                producto.stock += detalle.cantidad

        factura.estado = "anulada"
        self.db.commit()
        self.db.refresh(factura)
        return factura


    def obtener_detalles_por_factura(self, factura_id: UUID) -> List[DetalleFactura]:
        """Lista todos los ítems de una factura."""
        return (
            self.db.query(DetalleFactura)
            .filter(DetalleFactura.id_factura == factura_id)
            .all()
        )
