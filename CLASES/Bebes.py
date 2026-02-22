from CLASES.Producto import Producto


class Bebes(Producto):
    """
    Clase que representa un producto de la categoría Bebés.
    Hereda de la clase Producto y agrega atributos específicos
    como la categoría del producto para bebé y el rango de edad recomendado.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        marca: str,
        precio: float,
        stock: int,
        categoria_bebe: str,
        rango_edad: str,
    ) -> None:
        """
        Inicializa un producto de tipo Bebés.

        :param codigo: Código único del producto.
        :param nombre: Nombre del producto.
        :param marca: Marca del producto.
        :param precio: Precio del producto.
        :param stock: Cantidad disponible en inventario.
        :param categoria_bebe: Categoría del producto (ej: Pañales, Alimentación, Juguetes).
        :param rango_edad: Rango de edad recomendado (ej: 0-6 meses, 6-12 meses).
        :return: None
        """

        super().__init__(codigo, nombre, marca, precio, stock)
        self.categoria_bebe: str = categoria_bebe
        self.rango_edad: str = rango_edad

    def obtener_info(self) -> str:
        """
        Devuelve una representación formateada con la información
        principal del producto de bebés.
        """
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Categoría: {self.categoria_bebe} | Edad: {self.rango_edad}"
        )

    def _atributos_extra(self) -> list:
        """
        Retorna una lista de atributos adicionales específicos
        del producto de bebés.
        """

        return [
            ("CATEGORÍA", self.categoria_bebe),
            ("RANGO EDAD", self.rango_edad),
        ]

    def __str__(self) -> str:
        """
        Devuelve la representación en texto del objeto Bebes.
        """
        return self.obtener_info()
