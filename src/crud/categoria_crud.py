from src.entities.categoria import Categoria
from src.entities.usuario import Usuario
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

class CategoriaCrud:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(
        self, nombre: str, descripcion: str = None, usuario_id: UUID = None
    ) -> Categoria:
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre de la categoría es obligatorio")

        categoria_existente = (
            self.db.query(Categoria).filter(Categoria.nombre == nombre).first()
        )
        if categoria_existente is not None:
            raise ValueError(f"La categoría '{nombre}' ya existe")

        categoria = Categoria(
            nombre=nombre.strip(),
            descripcion=descripcion,
            id_usuario_creacion=usuario_id,
        )
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categorias(self) -> List[Categoria]:
        return self.db.query(Categoria).all()

    def obtener_categoria_por_id(self, categoria_id: UUID):
        return (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == categoria_id)
            .first()
        )

    def obtener_categoria_por_nombre(self, nombre: str):
        return self.db.query(Categoria).filter(Categoria.nombre == nombre).first()

    def actualizar_categoria(
        self, categoria_id: UUID, usuario_id: UUID, **kwargs
    ) -> Optional[Categoria]:

        categoria = self.obtener_categoria_por_id(categoria_id)

        if not categoria:
            return None

        for key, value in kwargs.items():
            if hasattr(categoria, key):
                setattr(categoria, key, value)

        categoria.id_usuario_edita = usuario_id

        self.db.commit()
        self.db.refresh(categoria)

        return categoria
   
    def eliminar_categoria(self,categoria_id:UUID)->bool:
        categoria =self.obtener_categoria_por_id(categoria_id)
        
        if not categoria:
            return False
        
        self.db.delete(categoria)
        self.db.commit()
        
        return True
