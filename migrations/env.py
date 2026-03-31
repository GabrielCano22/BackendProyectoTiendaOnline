import os
from logging.config import fileConfig
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

from src.database.config import Base
from src.entities.usuario import Usuario
from src.entities.tienda import Tienda
from src.entities.catalogo import Catalogo
from src.entities.categoria import Categoria
from src.entities.producto import Producto
from src.entities.descuento import Descuento
from src.entities.carrito import Carrito
from src.entities.detalle_carrito import DetalleCarrito
from src.entities.factura import Factura
from src.entities.detalle_factura import DetalleFactura

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
