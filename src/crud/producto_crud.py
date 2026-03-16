from src.entities.producto import Producto
from src.entities.categoria import Categoria
from src.entities.usuario import Usuario
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session


class ProductoCrud:
    def __init__(self, db: Session):  
        self.db = db

    def crear_producto(
        self,
        nombre: str,
        tipo_producto: str,
        codigo: str,
        marca: str,
        precio: float,
        categoria_id: UUID,
        usuario_id: UUID,
        descripcion: str = None,
        stock: int = 0,
    ) -> Producto:
        if not nombre or not tipo_producto or not codigo or not marca:
            raise ValueError("Nombre,tipo,codigo y marca son obligatorios")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        codigo_existente = (
            self.db.query(Producto).filter(Producto.codigo == codigo).first()
        )

        if codigo_existente is not None:
            raise ValueError(f"Ya existe un producto con el código '{codigo}'")

        categoria = (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == categoria_id)
            .first()
        )

        if not categoria:
            raise ValueError("La categoría especificada no existe")

        producto = Producto(
            nombre=nombre.strip(),
            tipo_producto=tipo_producto.strip(),
            codigo=codigo.strip().upper(),
            marca=marca.strip(),
            precio=precio,
            stock=stock,
            descripcion=descripcion,
            categoria_id=categoria_id,
            id_usuario_creacion=usuario_id,
        )

        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_productos(self) -> List[Producto]:
        return self.db.query(Producto).filter(Producto.eliminado == False).all()

    def obtener_producto_por_id(self, producto_id: UUID):
        return (
            self.db.query(Producto)
            .filter(Producto.id_producto == producto_id, Producto.eliminado == False)
            .first()
        )

    def obtener_producto_por_codigo(self, codigo: str):
        return (
            self.db.query(Producto)
            .filter(Producto.codigo == codigo.upper(), Producto.eliminado == False)
            .first()
        )
  
    def obtener_productos_por_categoria(self, categoria_id: UUID) -> List[Producto]:
        return (self.db.query(Producto).filter(Producto.categoria_id == categoria_id,Producto.eliminado == False).all())    

    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        return (
            self.db.query(Producto)
            .filter(Producto.nombre.ilike(f"%{nombre}%"), Producto.eliminado == False)
            .all()
        )

    def actualizar_producto(
        self, producto_id: UUID, usuario_id: UUID, **kwargs
    ) -> Optional[Producto]:

        producto = self.obtener_producto_por_id(producto_id)

        if not producto:
            return None

        if "precio" in kwargs and kwargs["precio"] <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if "stock" in kwargs and kwargs["stock"] < 0:
            raise ValueError("El stock no puede ser negativo")

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)

        producto.id_usuario_edita = usuario_id

        self.db.commit()
        self.db.refresh(producto)
        return producto
    
    def eliminar_producto(self, producto_id: UUID, usuario_id: UUID) -> bool:

    
        producto = self.obtener_producto_por_id(producto_id)

   
        if not producto:
            return False

        producto.eliminado = True
        producto.id_usuario_edita = usuario_id

   
        self.db.commit()

        return True