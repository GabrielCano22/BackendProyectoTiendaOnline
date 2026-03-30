"""
Manejadores de errores para FastAPI
"""
 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
 
from src.core.exceptions import AppException
 
 
def registrar_error_handlers(app: FastAPI):
    """Registra los manejadores de errores en la aplicacion FastAPI"""
 
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.codigo_http,
            content={
                "mensaje": exc.mensaje,
                "exito": False,
            },
        )
 
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={
                "mensaje": str(exc),
                "exito": False,
            },
        )
 
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "mensaje": "Error interno del servidor",
                "exito": False,
            },
        )