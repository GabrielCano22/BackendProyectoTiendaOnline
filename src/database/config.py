"""
Configuración de la base de datos PostgreSQL con Neon
"""

from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.database.engine_options import build_engine_options

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

engine = create_engine(
    DATABASE_URL,
    **build_engine_options(serverless=bool(os.getenv("VERCEL"))),
    connect_args={"sslmode": "require", "keepalives": 1, "keepalives_idle": 30, "keepalives_interval": 10, "keepalives_count": 5,},  # Requerir SSL para Neon
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    Elimina todas las tablas y las recrea con el esquema actual.
    Útil en desarrollo cuando el esquema de la BD no coincide con los modelos.
    """
    Base.metadata.create_all(bind=engine)
