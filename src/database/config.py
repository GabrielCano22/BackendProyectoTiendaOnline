"""
Configuración de la base de datos PostgreSQL con Neon
"""

from pathlib import Path


import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# Configuración de la base de datos Neon PostgreSQL
# Obtener la URL completa de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para ver consultas SQL
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=60,  # Reciclar conexiones cada minuto
    max_overflow=2,
    connect_args={"sslmode": "require", "keepalives": 1, "keepalives_idle": 30, "keepalives_interval": 10, "keepalives_count": 5,},  # Requerir SSL para Neon
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    Base.metadata.create_all(bind=engine)
