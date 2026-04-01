"""
Excepciones personalizadas para La Tienda de Gerardo
"""
 
class AppException(Exception):
    """Excepcion base de la aplicacion"""
    def __init__(self, mensaje: str, codigo_http: int = 400):
        self.mensaje = mensaje
        self.codigo_http = codigo_http
        super().__init__(self.mensaje)
 
class UsuarioNoEncontrado(AppException):
    def __init__(self, mensaje: str = "Usuario no encontrado"):
        super().__init__(mensaje, codigo_http=404)
 
class CredencialesInvalidas(AppException):
    def __init__(self, mensaje: str = "Credenciales incorrectas o usuario inactivo"):
        super().__init__(mensaje, codigo_http=401)
 
class UsuarioYaExiste(AppException):
    def __init__(self, mensaje: str = "El usuario ya esta registrado"):
        super().__init__(mensaje, codigo_http=400)
 
class DatosInvalidos(AppException):
    def __init__(self, mensaje: str = "Datos invalidos"):
        super().__init__(mensaje, codigo_http=400)
 
class ProductoNoEncontrado(AppException):
    def __init__(self, mensaje: str = "Producto no encontrado"):
        super().__init__(mensaje, codigo_http=404)
 
class CategoriaNoEncontrada(AppException):
    def __init__(self, mensaje: str = "Categoria no encontrada"):
        super().__init__(mensaje, codigo_http=404)
 
class StockInsuficiente(AppException):
    def __init__(self, mensaje: str = "Stock insuficiente"):
        super().__init__(mensaje, codigo_http=400)
 
class CarritoNoEncontrado(AppException):
    def __init__(self, mensaje: str = "Carrito no encontrado"):
        super().__init__(mensaje, codigo_http=404)
 
class FacturaNoEncontrada(AppException):
    def __init__(self, mensaje: str = "Factura no encontrada"):
        super().__init__(mensaje, codigo_http=404)
 
class OperacionNoPermitida(AppException):
    def __init__(self, mensaje: str = "Operacion no permitida"):
        super().__init__(mensaje, codigo_http=403)