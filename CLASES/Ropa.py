from CLASES.Producto import Producto
class Ropa(Producto):
    def __init__(self,codigo:str,nombre:str,  marca: str, precio: float, stock: int, tipo: str, talla: str, color: str)-> None:
        """
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.tipo: str = tipo
        self.talla: str = talla
        self.color: str = color
    
    def obtener_info(self) -> str:
        """
        Devuelve una representación formateada con la información
        principal del producto de ropa.
        """
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Tipo: {self.tipo} | Talla: {self.talla} | Color: {self.color}"
        )

    def _atributos_extra(self) -> list:
        """
        Retorna una lista de atributos adicionales específicos
        del producto de ropa.
        """
        return [
            ("TIPO", self.tipo),
            ("TALLA", self.talla),
            ("COLOR", self.color),
        ]
    def __str__(self) -> str:
        """Devuelve la representación en texto del objeto Ropa.
        """
        return self.obtener_info()
    


