from CLASES.Producto import Producto


class Hogar(Producto):
    """
    Clase que representa un producto de la categoría Hogar.
    Hereda de la clase Producto y añade atributos específicos
    como la categoría del hogar y la habitación a la que pertenece.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        marca: str,
        precio: float,
        stock: int,
        categoria_hogar: str,
        habitacion: str,
    ) -> None:
        """
        Inicializa un producto de tipo Hogar.

        :param codigo: Código único del producto.
        :param nombre: Nombre del producto.
        :param marca: Marca del producto.
        :param precio: Precio del producto.
        :param stock: Cantidad disponible en inventario.
        :param categoria_hogar: Tipo de producto del hogar
        (ej. decoración, muebles, iluminación).
        :param habitacion: Habitación donde se utiliza
        (ej. sala, cocina, dormitorio).
        :return: None
        """
        super().__init__(codigo, nombre, marca, precio, stock)
        self.categoria_hogar: str = categoria_hogar
        self.habitacion: str = habitacion

    def obtener_info(self) -> str:
        """
        Devuelve una representación formateada con la información
        principal del producto de hogar.

        """
        return (
            f"[{self.codigo}] {self.nombre} | Marca: {self.marca} "
            f"| Categoría: {self.categoria_hogar} | Habitación: {self.habitacion}"
        )

    def _atributos_extra(self) -> list:
        """
        Retorna una lista de atributos adicionales específicos
        del producto de hogar.

        :return: Lista de tuplas con el nombre del atributo
         y su valor correspondiente.
        """

        return [
            ("CATEGORÍA", self.categoria_hogar),
            ("HABITACIÓN", self.habitacion),
        ]

    def __str__(self) -> str:
        return self.obtener_info()
