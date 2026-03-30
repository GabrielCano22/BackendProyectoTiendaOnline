"""
Respuestas estandarizadas para la API
"""
 
from typing import Any, Optional
 
from pydantic import BaseModel
 
 
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[Any] = None