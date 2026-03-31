"""
Endpoints de Facturas
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.crud.factura_crud import FacturaCrud
from src.database.config import get_db
from schemas import FacturaResponse

router = APIRouter(prefix="/facturas", tags=["facturas"])

@router.post("/{id_usuario}/generar", response_model=FacturaResponse, status_code=201)
async def generar_factura(id_usuario: UUID, db: Session = Depends(get_db)):
    """Genera una factura a partir del carrito activo del usuario."""
    from src.crud.carrito_crud import CarritoCrud

    carrito_crud = CarritoCrud(db)
    carrito = carrito_crud.obtener_carrito_activo(id_usuario)
    if not carrito or not carrito.detalles:
        raise HTTPException(400, "No hay carrito activo o el carrito está vacío")

    try:
        factura = FacturaCrud(db).generar_factura(carrito.id_carrito, id_usuario)
        return factura
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{id_usuario}", response_model=List[FacturaResponse])
async def historial_facturas(id_usuario: UUID, db: Session = Depends(get_db)):
    """Obtiene el historial de facturas del usuario."""
    return FacturaCrud(db).obtener_facturas_por_usuario(id_usuario)

@router.get("/detalle/{id_factura}", response_model=FacturaResponse)
async def ver_factura(id_factura: UUID, db: Session = Depends(get_db)):
    """Obtiene el detalle de una factura específica."""
    factura = FacturaCrud(db).obtener_factura_por_id(id_factura)
    if not factura:
        raise HTTPException(404, "Factura no encontrada")
    return factura