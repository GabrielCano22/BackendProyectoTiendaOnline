"""
Endpoints de Categorías
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.categoria_crud import CategoriaCrud
from src.database.config import get_db
from schemas import CategoriaCreate, CategoriaUpdate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=List[CategoriaResponse])
async def listar_categorias(db: Session = Depends(get_db)):
    crud = CategoriaCrud(db)
    return crud.obtener_categorias()


@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def obtener_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    crud = CategoriaCrud(db)
    categoria = crud.obtener_categoria_por_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.post("/", response_model=CategoriaResponse)
async def crear_categoria(data: CategoriaCreate, db: Session = Depends(get_db)):
    crud = CategoriaCrud(db)
    try:
        return crud.crear_categoria(
            nombre=data.nombre,
            descripcion=data.descripcion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def actualizar_categoria(
    categoria_id: UUID, data: CategoriaUpdate, db: Session = Depends(get_db)
):
    crud = CategoriaCrud(db)
    campos = {k: v for k, v in data.model_dump().items() if v is not None}
    try:
        categoria = crud.actualizar_categoria(categoria_id, usuario_id=None, **campos)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return categoria
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{categoria_id}")
async def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    crud = CategoriaCrud(db)
    if not crud.eliminar_categoria(categoria_id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": "Categoría eliminada exitosamente"}
