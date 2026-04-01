"""
Endpoints de Categorías
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.crud.categoria_crud import CategoriaCrud
from src.database.config import get_db
from src.core.responses import RespuestaAPI
from schemas import CategoriaCreate, CategoriaResponse, CategoriaUpdate

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=List[CategoriaResponse])
async def listar_categorias(db: Session = Depends(get_db)):
    """Lista todas las categorías."""
    crud = CategoriaCrud(db)
    return crud.obtener_categorias()

@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def obtener_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una categoría por su ID."""
    crud = CategoriaCrud(db)
    categoria = crud.obtener_categoria_por_id(categoria_id)
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    return categoria

@router.post("/", response_model=CategoriaResponse, status_code=201)
async def crear_categoria(
    data: CategoriaCreate, usuario_id: UUID, db: Session = Depends(get_db)
):
    """Crea una nueva categoría."""
    crud = CategoriaCrud(db)
    try:
        categoria = crud.crear_categoria(
            nombre=data.nombre,
            descripcion=data.descripcion,
            usuario_id=usuario_id,
        )
        return categoria
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def actualizar_categoria(
    categoria_id: UUID,
    data: CategoriaUpdate,
    usuario_id: UUID,
    db: Session = Depends(get_db),
):
    """Actualiza una categoría existente."""
    crud = CategoriaCrud(db)
    campos = {k: v for k, v in data.dict().items() if v is not None}
    try:
        categoria = crud.actualizar_categoria(categoria_id, usuario_id, **campos)
        if not categoria:
            raise HTTPException(404, "Categoría no encontrada")
        return categoria
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/{categoria_id}", response_model=RespuestaAPI)
async def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    """Elimina una categoría."""
    crud = CategoriaCrud(db)
    if not crud.eliminar_categoria(categoria_id):
        raise HTTPException(404, "Categoría no encontrada")
    return RespuestaAPI(mensaje="Categoría eliminada", exito=True)