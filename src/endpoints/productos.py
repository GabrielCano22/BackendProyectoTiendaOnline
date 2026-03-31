"""
Endpoints de Productos
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.producto_crud import ProductoCrud
from src.database.config import get_db
from schemas import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoResponse])
async def listar_productos(db: Session = Depends(get_db)):
    crud = ProductoCrud(db)
    return crud.obtener_productos()


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    crud = ProductoCrud(db)
    producto = crud.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.get("/codigo/{codigo}", response_model=ProductoResponse)
async def obtener_producto_por_codigo(codigo: str, db: Session = Depends(get_db)):
    crud = ProductoCrud(db)
    producto = crud.obtener_producto_por_codigo(codigo)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.get("/buscar/{nombre}", response_model=List[ProductoResponse])
async def buscar_productos_por_nombre(nombre: str, db: Session = Depends(get_db)):
    crud = ProductoCrud(db)
    return crud.buscar_productos_por_nombre(nombre)


@router.post("/", response_model=ProductoResponse)
async def crear_producto(data: ProductoCreate, db: Session = Depends(get_db)):
    crud = ProductoCrud(db)
    try:
        return crud.crear_producto(
            nombre=data.nombre,
            tipo_producto=data.tipo_producto,
            codigo=data.codigo,
            marca=data.marca,
            precio=data.precio,
            stock=data.stock,
            descripcion=data.descripcion,
            categoria_id=data.categoria_id,
            usuario_id=None,  # en esta fase aún no tenemos autenticación conectada a los endpoints. Cuando Gabriel termine la autenticación se reemplazará None por el usuario que está haciendo la petición.
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: UUID, data: ProductoUpdate, db: Session = Depends(get_db)
):
    crud = ProductoCrud(db)
    campos = {k: v for k, v in data.model_dump().items() if v is not None}
    try:
        producto = crud.actualizar_producto(producto_id, usuario_id=None, **campos)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    crud = ProductoCrud(db)
    if not crud.eliminar_producto(producto_id, usuario_id=None):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado exitosamente"}
