"""
CRUD para Usuario, Cliente y Administrador
"""

import re
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.auth.security import PasswordManager
from src.entities.usuario import Administrador, Cliente, Usuario

def _validar_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cliente(self, nombre: str, nombre_usuario: str, email: str,
                  contrasena: str, telefono: str = None) -> Cliente:
        self._validar_datos(nombre, nombre_usuario, email, contrasena)
        usuario = Cliente(
            nombre=nombre.strip(),
            nombre_usuario=nombre_usuario.strip().lower(),
            email=email.lower().strip(),
            contrasena_hash=PasswordManager.hash_password(contrasena),
            telefono=telefono.strip() if telefono else None,
            rol="cliente",
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def crear_administrador(self, nombre: str, nombre_usuario: str, email: str,
                            contrasena: str, telefono: str = None) -> Administrador:
       self._validar_datos(nombre, nombre_usuario, email, contrasena)
       admin = Administrador(
           nombre=nombre.strip(),
           nombre_usuario=nombre_usuario.strip().lower(),
           email=email.lower().strip(),
           contrasena_hash=PasswordManager.hash_password(contrasena),
           telefono=telefono.strip() if telefono else None,
           rol="administrador",
       )
       self.db.add(admin)
       self.db.commit()
       self.db.refresh(admin)
       return admin

    def _validar_datos(self, nombre, nombre_usuario, email, contrasena):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        if not nombre_usuario or len(nombre_usuario.strip()) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        if not email or not _validar_email(email):
            raise ValueError("Email invalido")
        es_valida, mensaje = PasswordManager.validate_password_strength(contrasena)
        if not es_valida:
            raise ValueError(f"Contrasena invalida: {mensaje}")
        if self.obtener_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya esta registrado")
        if self.obtener_por_email(email):
            raise ValueError("El email ya esta registrado")
        
    def obtener_por_id(self, id_usuario: UUID) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email.lower().strip()).first()
 
    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario.lower().strip())
            .first()
        )

    def autenticar(self, nombre_usuario: str, contrasena: str) -> Optional[Usuario]:
        usuario = self.obtener_por_nombre_usuario(nombre_usuario)
        if not usuario:
            usuario = self.obtener_por_email(nombre_usuario)
        if not usuario or not usuario.activo:
            return None
        if PasswordManager.verify_password(contrasena, usuario.contrasena_hash):
            return usuario
        return None

    def es_admin(self, usuario: Usuario) -> bool:
        return usuario.rol == "administrador"
    
    def listar(self) -> List[Usuario]:
        return self.db.query(Usuario).filter(Usuario.activo == True).all()

    def listar_clientes(self) -> List[Cliente]:
        return self.db.query(Cliente).filter(Cliente.activo == True).all()

    def actualizar(self, id_usuario: UUID, **kwargs) -> Optional[Usuario]:
        usuario = self.obtener_por_id(id_usuario)
        
        if not usuario:
            return None
        if "email" in kwargs:
            if not _validar_email(kwargs["email"]):
                raise ValueError("Email invalido")
            kwargs["email"] = kwargs["email"].lower().strip()
        if "nombre" in kwargs:
            kwargs["nombre"] = kwargs["nombre"].strip()
        for k, v in kwargs.items():
            if hasattr(usuario, k):
                setattr(usuario, k, v)
        self.db.commit()
        self.db.refresh(usuario)
        
        return usuario

    def eliminar(self, id_usuario: UUID) -> bool:
        usuario = self.obtener_por_id(id_usuario)
        
        if not usuario:
            return False
        self.db.delete(usuario)
                
        self.db.commit()
        return True
 
    def desactivar(self, id_usuario: UUID) -> bool:
        usuario = self.obtener_por_id(id_usuario)
        if not usuario:
            return False
        
        usuario.activo = False
        self.db.commit()
        
        return True
    
 
    def hay_administradores(self) -> bool:
        return self.db.query(Administrador).count() > 0