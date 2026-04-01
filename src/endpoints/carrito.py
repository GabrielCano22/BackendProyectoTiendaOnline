"""
Endpoints de Carrito de Compras
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.carrito_crud import CarritoCrud
from src.crud.producto_crud import ProductoCrud
from src.database.config import get_db
from src.core.responses import RespuestaAPI
from schemas import (
    AgregarAlCarritoRequest,
    ActualizarCantidadRequest,
    CarritoResponse,
)

router = APIRouter(prefix="/carrito", tags=["carrito"])

def _obtener_o_crear_carrito(id_usuario: UUID, db: Session):
    crud = CarritoCrud(db)
    carrito = crud.obtener_carrito_activo(id_usuario)
    if not carrito:
        carrito = crud.crear_carrito(id_usuario)
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
    carrito_crud = CarritoCrud(db)
    producto_crud = ProductoCrud(db)

    producto = producto_crud.obtener_producto_por_id(data.id_producto)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    if producto.stock < data.cantidad:
        raise HTTPException(400, f"Stock insuficiente. Disponible: {producto.stock}")

    carrito = _obtener_o_crear_carrito(id_usuario, db)
    try:
        carrito_crud.agregar_producto(
            carrito_id=carrito.id_carrito,
            producto_id=data.id_producto,
            cantidad=data.cantidad,
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
    carrito_crud = CarritoCrud(db)
    carrito = carrito_crud.obtener_carrito_activo(id_usuario)
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
    carrito_crud = CarritoCrud(db)
    carrito = carrito_crud.obtener_carrito_activo(id_usuario)
    if not carrito:
        raise HTTPException(404, "No hay carrito activo")
    carrito_crud.eliminar_producto(carrito.id_carrito, id_producto)
    db.refresh(carrito)
    return carrito

@router.delete("/{id_usuario}/vaciar", response_model=RespuestaAPI)
async def vaciar_carrito(id_usuario: UUID, db: Session = Depends(get_db)):
    """Vacía completamente el carrito."""
    carrito_crud = CarritoCrud(db)
    carrito = carrito_crud.obtener_carrito_activo(id_usuario)
    if not carrito:
        raise HTTPException(404, "No hay carrito activo")
    carrito_crud.vaciar_carrito(carrito.id_carrito)
    return RespuestaAPI(mensaje="Carrito vaciado", exito=True)