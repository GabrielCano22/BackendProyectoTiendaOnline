from src.entities.usuario import Usuario
import hashlib
import re
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session


class UsuarioCrud:
    def __init__(self, db: Session):
        self.db = db

    def _hash_clave(self, clave: str) -> str:
        return hashlib.sha256(clave.encode()).hexdigest()

    def _verificar_clave(self, clave: str, hash_guardado: str) -> bool:
        return hashlib.sha256(clave.encode()).hexdigest() == hash_guardado

    def crear_usuario(
        self,
        nombre_completo: str,
        nombre_usuario: str,
        email: str,
        clave: str,
        telefono: str = None,
        es_admin: bool = False,
    ) -> Usuario:

        if not nombre_completo or not nombre_usuario or not email or not clave:
            raise ValueError("Todos los campos son obligatorios ")

        usuario_existente = (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario)
            .first()
        )

        if usuario_existente is not None:
            raise ValueError(f"El usuario '{nombre_usuario}' ya existe")

        email_existente = self.db.query(Usuario).filter(Usuario.email == email).first()

        if email_existente is not None:
            raise ValueError(f"el email '{email}' ya existe")

        usuario = Usuario(
            nombre_completo=nombre_completo.strip(),
            nombre_usuario=nombre_usuario.strip(),
            email=email.strip().lower(),
            clave=self._hash_clave(clave),
            telefono=telefono,
            es_admin=es_admin,
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def autenticar_usuario(self, nombre_usuario: str, clave: str):

        usuario = (
            self.db.query(Usuario)
            .filter(
                (Usuario.nombre_usuario == nombre_usuario)
                | (Usuario.email == nombre_usuario)
            )
            .first()
        )
        
        if not usuario:
            return None
        
        if not usuario.activo:
            return None 
        if not self._verificar_clave(clave, usuario.clave):
            return None
        
        return usuario
    
    def obtener_usuario (self, usuario_id:UUID):
        return (self.db.query(Usuario).filter(Usuario.id_usuario==usuario_id).first())
    
    def obtener_usuarios (self)-> List[Usuario]:
        return self.db.query(Usuario).all()
        
    
    
    def actualizar_usuarios(self, usuario_id: UUID, **kwargs):
        usuario=self.obtener_usuario(usuario_id)
        
        if not usuario:
            return None
        
        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario,key,value)
                
        self.db.commit()
        self.db.refresh(usuario)
        
        return usuario        
    
    def eliminar_usuario(self,usuario_id:UUID) ->bool:
        usuario = self.obtener_usuario(usuario_id)     
        
        if not usuario:
            return False
        
        usuario.activo = False
        self.db.commit()
        
        return True
    
    def obtener_admin(self):
        return(self.db.query(Usuario).filter(Usuario.es_admin==True).first())
    
