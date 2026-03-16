"""Migración inicial - todas las entidades de La Tienda de Gerardo

Revision ID: 001_initial
Revises:
Create Date: 2026-03-16
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id_usuario", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nombre_completo", sa.String(100), nullable=False),
        sa.Column("nombre_usuario", sa.String(50), nullable=False),
        sa.Column("email", sa.String(150), nullable=False),
        sa.Column("clave", sa.String(255), nullable=False),
        sa.Column("telefono", sa.String(20), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True, server_default=sa.text("true")),
        sa.Column("es_admin", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("fecha_edicion", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id_usuario"),
    )
    op.create_index("ix_usuarios_id_usuario", "usuarios", ["id_usuario"], unique=False)
    op.create_index("ix_usuarios_nombre_usuario", "usuarios", ["nombre_usuario"], unique=True)
    op.create_index("ix_usuarios_email", "usuarios", ["email"], unique=True)
    
    op.create_table(
        "descuentos",
        sa.Column("id_descuento", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("descripcion", sa.String(100), nullable=False),
        sa.Column("unidades_minimas", sa.Integer(), nullable=False),
        sa.Column("porcentaje", sa.Numeric(5, 2), nullable=False),
        sa.PrimaryKeyConstraint("id_descuento"),
    )
    op.create_index("ix_descuentos_id_descuento", "descuentos", ["id_descuento"], unique=False)

    op.create_table(
        "tiendas",
        sa.Column("id_tienda", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.PrimaryKeyConstraint("id_tienda"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index("ix_tiendas_id_tienda", "tiendas", ["id_tienda"], unique=False)

    op.create_table(
        "catalogos",
        sa.Column("id_catalogo", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_tienda", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("descripcion", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(["id_tienda"], ["tiendas.id_tienda"]),
        sa.PrimaryKeyConstraint("id_catalogo"),
        sa.UniqueConstraint("id_tienda"),
    )
    op.create_index("ix_catalogos_id_catalogo", "catalogos", ["id_catalogo"], unique=False)

    op.create_table(
        "categorias",
        sa.Column("id_categoria", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("fecha_edicion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id_usuario_creacion", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_usuario_edita", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["id_usuario_creacion"], ["usuarios.id_usuario"]),
        sa.ForeignKeyConstraint(["id_usuario_edita"], ["usuarios.id_usuario"]),
        sa.PrimaryKeyConstraint("id_categoria"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index("ix_categorias_id_categoria", "categorias", ["id_categoria"], unique=False)

    op.create_table(
        "productos",
        sa.Column("id_producto", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nombre", sa.String(200), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("tipo_producto", sa.String(50), nullable=False),
        sa.Column("codigo", sa.String(20), nullable=False),
        sa.Column("marca", sa.String(100), nullable=False),
        sa.Column("precio", sa.Numeric(10, 2), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("eliminado", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("categoria_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_catalogo", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("fecha_edicion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id_usuario_creacion", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_usuario_edita", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id_categoria"]),
        sa.ForeignKeyConstraint(["id_catalogo"], ["catalogos.id_catalogo"]),
        sa.ForeignKeyConstraint(["id_usuario_creacion"], ["usuarios.id_usuario"]),
        sa.ForeignKeyConstraint(["id_usuario_edita"], ["usuarios.id_usuario"]),
        sa.PrimaryKeyConstraint("id_producto"),
        sa.UniqueConstraint("codigo"),
    )
    op.create_index("ix_productos_id_producto", "productos", ["id_producto"], unique=False)
    op.create_index("ix_productos_codigo", "productos", ["codigo"], unique=True)


def downgrade() -> None:
    op.drop_table("productos")
    op.drop_table("categorias")
    op.drop_table("catalogos")
    op.drop_table("tiendas")
    op.drop_table("descuentos")
    op.drop_table("usuarios")