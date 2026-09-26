#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La Tienda de Gerardo — Backend FastAPI
"""
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.config import create_tables, get_db
from src.core.error_handlers import registrar_error_handlers
from src.endpoints.auth import router as auth_router
from src.endpoints.usuarios import router as usuarios_router
from src.endpoints.carrito import router as carrito_router
from src.endpoints.facturas import router as facturas_router
from src.endpoints.productos import router as productos_router
from src.endpoints.categorias import router as categorias_router
from src.endpoints.descuentos_tienda import router as descuentos_router
from src.crud.tienda_crud import TiendaCrud
from src.crud.descuento_crud import DescuentoCrud
from src.crud.usuario_crud import UsuarioCRUD
from src.core.runtime_settings import cors_origins, should_run_startup_initialization

app = FastAPI(
    title="La Tienda de Gerardo — API",
    description="API REST completa: usuarios, productos, carrito, facturas y más.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(os.getenv("CORS_ORIGINS")),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

registrar_error_handlers(app)

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(carrito_router)
app.include_router(facturas_router)

app.include_router(productos_router)
app.include_router(categorias_router)
app.include_router(descuentos_router)

@app.on_event("startup")
async def startup():
    print("🚀 Iniciando La Tienda de Gerardo...")
    if not should_run_startup_initialization(
        vercel=bool(os.getenv("VERCEL")),
        configured=os.getenv("RUN_STARTUP_INITIALIZATION"),
    ):
        print("ℹ️ Inicialización de base de datos omitida en este entorno")
        return

    create_tables()

    db = next(get_db())
    try:
        TiendaCrud(db).inicializar()
        DescuentoCrud(db).seed_descuentos_base()

        crud_u = UsuarioCRUD(db)
        admin_password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD")
        if not crud_u.hay_administradores() and admin_password:
            crud_u.crear_administrador(
                nombre=os.getenv("BOOTSTRAP_ADMIN_NAME", "Administrador"),
                nombre_usuario=os.getenv("BOOTSTRAP_ADMIN_USERNAME", "admin"),
                email=os.getenv("BOOTSTRAP_ADMIN_EMAIL", "admin@tienda.com"),
                contrasena=admin_password,
            )
            print("✅ Administrador inicial creado desde variables de entorno")
    finally:
        db.close()

    print("✅ Sistema listo en http://localhost:8000")
    print("📚 Docs en http://localhost:8000/docs")

@app.get("/", tags=["raíz"])
async def root():
    return {
        "mensaje": "La Tienda de Gerardo — API v1.0",
        "docs": "/docs",
        "endpoints_activos": {
            "auth": "/auth",
            "usuarios": "/usuarios",
            "productos": "/productos",
            "categorias": "/categorias",
            "descuentos": "/descuentos",
            "tienda": "/tienda",
            "carrito": "/carrito",
            "facturas": "/facturas",
        },
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
