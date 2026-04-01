"""
Endpoints de Productos
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user, require_admin
from src.crud.producto_crud import ProductoCrud
from src.database.config import get_db
from src.core.responses import RespuestaAPI
from src.entities.usuario import Usuario
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoResponse])
async def listar_productos(db: Session = Depends(get_db)):
    """Lista todos los productos activos."""
    crud = ProductoCrud(db)
    return crud.obtener_productos()


@router.get("/buscar/{nombre}", response_model=List[ProductoResponse])
async def buscar_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Busca productos cuyo nombre coincida parcialmente."""
    crud = ProductoCrud(db)
    return crud.buscar_productos_por_nombre(nombre)


@router.get("/codigo/{codigo}", response_model=ProductoResponse)
async def obtener_por_codigo(codigo: str, db: Session = Depends(get_db)):
    """Obtiene un producto por su código."""
    crud = ProductoCrud(db)
    producto = crud.obtener_producto_por_codigo(codigo)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return producto


@router.get("/categoria/{categoria_id}", response_model=List[ProductoResponse])
async def listar_por_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    """Lista productos filtrados por categoría."""
    crud = ProductoCrud(db)
    return crud.obtener_productos_por_categoria(categoria_id)


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un producto por su ID."""
    crud = ProductoCrud(db)
    producto = crud.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoResponse, status_code=201)
async def crear_producto(
    data: ProductoCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(require_admin),
):
    """Crea un nuevo producto. Solo administradores."""
    crud = ProductoCrud(db)
    try:
        producto = crud.crear_producto(
            nombre=data.nombre,
            tipo_producto=data.tipo_producto,
            codigo=data.codigo,
            marca=data.marca,
            precio=float(data.precio),
            categoria_id=data.categoria_id,
            usuario_id=admin.id_usuario,
            descripcion=data.descripcion,
            stock=data.stock,
        )
        return producto
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: UUID,
    data: ProductoUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(require_admin),
):
    """Actualiza un producto existente. Solo administradores."""
    crud = ProductoCrud(db)
    campos = {k: v for k, v in data.dict().items() if v is not None}
    try:
        producto = crud.actualizar_producto(producto_id, admin.id_usuario, **campos)
        if not producto:
            raise HTTPException(404, "Producto no encontrado")
        return producto
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.delete("/{producto_id}", response_model=RespuestaAPI)
async def eliminar_producto(
    producto_id: UUID,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(require_admin),
):
    """Elimina (soft delete) un producto. Solo administradores."""
    crud = ProductoCrud(db)
    if not crud.eliminar_producto(producto_id, admin.id_usuario):
        raise HTTPException(404, "Producto no encontrado")
    return RespuestaAPI(mensaje="Producto eliminado", exito=True)
