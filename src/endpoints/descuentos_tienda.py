"""
Endpoints de Descuentos y Tienda
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.auth.dependencies import require_admin
from src.crud.descuento_crud import DescuentoCrud
from src.crud.tienda_crud import TiendaCrud
from src.database.config import get_db
from src.core.responses import RespuestaAPI
from src.entities.usuario import Usuario
from schemas import (
    CatalogoResponse,
    DescuentoCreate,
    DescuentoResponse,
    DescuentoUpdate,
    TiendaResponse,
)

router = APIRouter(tags=["descuentos y tienda"])

@router.get("/descuentos", response_model=List[DescuentoResponse])
async def listar_descuentos(db: Session = Depends(get_db)):
    """Lista todas las reglas de descuento ordenadas por unidades mínimas."""
    crud = DescuentoCrud(db)
    return crud.listar()

@router.get("/descuentos/{descuento_id}", response_model=DescuentoResponse)
async def obtener_descuento(descuento_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un descuento por su ID."""
    crud = DescuentoCrud(db)
    descuento = crud.obtener_por_id(descuento_id)
    if not descuento:
        raise HTTPException(404, "Descuento no encontrado")
    return descuento

@router.post("/descuentos", response_model=DescuentoResponse, status_code=201)
async def crear_descuento(
    data: DescuentoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    """Crea una nueva regla de descuento. Solo administradores."""
    crud = DescuentoCrud(db)
    try:
        descuento = crud.crear(
            descripcion=data.descripcion,
            unidades_minimas=data.unidades_minimas,
            porcentaje=data.porcentaje,
        )
        return descuento
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.put("/descuentos/{descuento_id}", response_model=DescuentoResponse)
async def actualizar_descuento(
    descuento_id: UUID,
    data: DescuentoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    """Actualiza una regla de descuento existente. Solo administradores."""
    crud = DescuentoCrud(db)
    campos = {k: v for k, v in data.dict().items() if v is not None}
    try:
        descuento = crud.actualizar(descuento_id, **campos)
        if not descuento:
            raise HTTPException(404, "Descuento no encontrado")
        return descuento
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/descuentos/{descuento_id}", response_model=RespuestaAPI)
async def eliminar_descuento(
    descuento_id: UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    """Elimina una regla de descuento. Solo administradores."""
    crud = DescuentoCrud(db)
    if not crud.eliminar(descuento_id):
        raise HTTPException(404, "Descuento no encontrado")
    return RespuestaAPI(mensaje="Descuento eliminado", exito=True)

@router.get("/tienda", response_model=TiendaResponse)
async def obtener_tienda(db: Session = Depends(get_db)):
    """Obtiene la información de la tienda principal."""
    crud = TiendaCrud(db)
    tienda = crud.obtener_tienda()
    if not tienda:
        raise HTTPException(404, "Tienda no inicializada")
    return tienda

@router.get("/tienda/catalogo", response_model=CatalogoResponse)
async def obtener_catalogo(db: Session = Depends(get_db)):
    """Obtiene el catálogo de la tienda."""
    crud = TiendaCrud(db)
    catalogo = crud.obtener_catalogo()
    if not catalogo:
        raise HTTPException(404, "Catálogo no encontrado")
    return catalogo