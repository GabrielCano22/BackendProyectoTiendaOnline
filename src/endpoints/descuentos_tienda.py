"""
Endpoints de Descuentos y Tienda
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.descuento_crud import DescuentoCrud
from src.crud.tienda_crud import TiendaCrud
from src.database.config import get_db
from schemas import (
    DescuentoCreate,
    DescuentoUpdate,
    DescuentoResponse,
    TiendaResponse,
    CatalogoResponse,
)

router = APIRouter(tags=["descuentos y tienda"])


@router.get("/descuentos/", response_model=List[DescuentoResponse])
async def listar_descuentos(db: Session = Depends(get_db)):
    crud = DescuentoCrud(db)
    return crud.listar()


@router.get("/descuentos/{descuento_id}", response_model=DescuentoResponse)
async def obtener_descuento(descuento_id: UUID, db: Session = Depends(get_db)):
    crud = DescuentoCrud(db)
    descuento = crud.obtener_por_id(descuento_id)
    if not descuento:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    return descuento


@router.post("/descuentos/", response_model=DescuentoResponse)
async def crear_descuento(data: DescuentoCreate, db: Session = Depends(get_db)):
    crud = DescuentoCrud(db)
    try:
        return crud.crear(
            descripcion=data.descripcion,
            unidades_minimas=data.unidades_minimas,
            porcentaje=data.porcentaje,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/descuentos/{descuento_id}", response_model=DescuentoResponse)
async def actualizar_descuento(
    descuento_id: UUID, data: DescuentoUpdate, db: Session = Depends(get_db)
):
    crud = DescuentoCrud(db)
    campos = {k: v for k, v in data.model_dump().items() if v is not None}
    try:
        descuento = crud.actualizar(descuento_id, **campos)
        if not descuento:
            raise HTTPException(status_code=404, detail="Descuento no encontrado")
        return descuento
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/descuentos/{descuento_id}")
async def eliminar_descuento(descuento_id: UUID, db: Session = Depends(get_db)):
    crud = DescuentoCrud(db)
    if not crud.eliminar(descuento_id):
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    return {"mensaje": "Descuento eliminado exitosamente"}


@router.get("/tienda/", response_model=TiendaResponse)
async def obtener_tienda(db: Session = Depends(get_db)):
    crud = TiendaCrud(db)
    tienda = crud.obtener_tienda()
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return tienda


@router.get("/tienda/catalogo/", response_model=CatalogoResponse)
async def obtener_catalogo(db: Session = Depends(get_db)):
    crud = TiendaCrud(db)
    catalogo = crud.obtener_catalogo()
    if not catalogo:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    return catalogo
