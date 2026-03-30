"""
Endpoints de Carrito de Compras
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.carrito_crud import CarritoCRUD
from src.crud.producto_crud import ProductoCRUD
from src.database.config import get_db
from src.core.responses import RespuestaAPI
from src.schemas import (
    AgregarAlCarritoRequest,
    ActualizarCantidadRequest,
    CarritoResponse,
)

router = APIRouter(prefix="/carrito", tags=["carrito"])


def _obtener_o_crear_carrito(id_usuario: UUID, db: Session):
    crud = CarritoCRUD(db)
    carrito = crud.obtener_activo(id_usuario)
    if not carrito:
        carrito = crud.crear(id_usuario)
    return carrito


@router.get("/{id_usuario}", response_model=CarritoResponse)
async def ver_carrito(id_usuario: UUID, db: Session = Depends(get_db)):
    """Obtiene el carrito activo del usuario, lo crea si no existe."""
    return _obtener_o_crear_carrito(id_usuario, db)


@router.post("/{id_usuario}/agregar", response_model=CarritoResponse)
async def agregar_producto(
    id_usuario: UUID, data: AgregarAlCarritoRequest, db: Session = Depends(get_db)
):
    """Agrega un producto al carrito. Si ya existe, suma la cantidad."""
    carrito_crud = CarritoCRUD(db)
    producto_crud = ProductoCRUD(db)

    producto = producto_crud.obtener_por_id(data.id_producto)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    if producto.stock < data.cantidad:
        raise HTTPException(400, f"Stock insuficiente. Disponible: {producto.stock}")

    carrito = _obtener_o_crear_carrito(id_usuario, db)
    try:
        carrito_crud.agregar_producto(
            id_carrito=carrito.id_carrito,
            id_producto=data.id_producto,
            cantidad=data.cantidad,
            precio_unitario=producto.precio,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    db.refresh(carrito)
    return carrito


@router.put("/{id_usuario}/actualizar/{id_producto}", response_model=CarritoResponse)
async def actualizar_cantidad(
    id_usuario: UUID,
    id_producto: UUID,
    data: ActualizarCantidadRequest,
    db: Session = Depends(get_db),
):
    """Actualiza la cantidad de un producto en el carrito."""
    carrito_crud = CarritoCRUD(db)
    carrito = carrito_crud.obtener_activo(id_usuario)
    if not carrito:
        raise HTTPException(404, "No hay carrito activo")
    try:
        carrito_crud.actualizar_cantidad(carrito.id_carrito, id_producto, data.cantidad)
    except ValueError as e:
        raise HTTPException(400, str(e))
    db.refresh(carrito)
    return carrito


@router.delete("/{id_usuario}/quitar/{id_producto}", response_model=CarritoResponse)
async def quitar_producto(
    id_usuario: UUID, id_producto: UUID, db: Session = Depends(get_db)
):
    """Quita un producto del carrito."""
    carrito_crud = CarritoCRUD(db)
    carrito = carrito_crud.obtener_activo(id_usuario)
    if not carrito:
        raise HTTPException(404, "No hay carrito activo")
    carrito_crud.eliminar_producto(carrito.id_carrito, id_producto)
    db.refresh(carrito)
    return carrito


@router.delete("/{id_usuario}/vaciar", response_model=RespuestaAPI)
async def vaciar_carrito(id_usuario: UUID, db: Session = Depends(get_db)):
    """Vacía completamente el carrito."""
    carrito_crud = CarritoCRUD(db)
    carrito = carrito_crud.obtener_activo(id_usuario)
    if not carrito:
        raise HTTPException(404, "No hay carrito activo")
    carrito_crud.vaciar(carrito.id_carrito)
    return RespuestaAPI(mensaje="Carrito vaciado", exito=True)
