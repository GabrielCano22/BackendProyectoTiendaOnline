from tienda import Tienda


class Carrito:
    def __init__(self) -> None:
        """
        Inicializa el carrito con un diccionario vacío de items.

        items: Diccionario donde la clave es el código del producto
        y el valor es otro diccionario con el producto y su cantidad.
        """
        self.items = {}

    def agregar_producto(self, tienda: Tienda, codigo: str, cantidad: int) -> None:
        """
        Agrega un producto al carrito si existe en la tienda
        y hay suficiente stock.

        :param tienda: Objeto de tipo Tienda.
        :param codigo: Código del producto.
        :param cantidad: Cantidad a agregar.
        :return: None
        """

        producto = tienda.buscar_por_codigo(codigo)

        if not producto:
            print("Producto no encontrado en la tienda.")
            return

        if producto.obtener_stock() < cantidad:
            print("No hay suficiente stock para agregar al carrito.")
            return
        if codigo in self.items:
            self.items[codigo]["cantidad"] += cantidad
            print("Producto agregado al carrito. Cantidad actualizada.")

        else:
            self.items[codigo] = {"producto": producto, "cantidad": cantidad}
            print(
                f"Producto '{producto.nombre}' agregado al carrito. Cantidad: {cantidad}."
            )
        producto.reducir_stock(cantidad)

    def vaciar_carrito(self) -> None:
        """
        Vacía completamente el carrito.

        :return: None
        """
        self.items = {}

    def mostrar_carrito(self) -> None:
        """
        Muestra los productos del carrito,
        calcula el total y aplica descuentos si corresponde.

        :return: None
        """
        if not self.items:
            print("El carrito se encuentra vacio.")
            return
        else:
            total = 0
            for codigo, item in self.items.items():
                producto = item["producto"]
                cantidad = item["cantidad"]
                subtotal = producto.obtener_precio() * cantidad
                total += subtotal

                print(
                    f"|{producto.nombre} |(x{cantidad})|  ${producto.obtener_precio():} COP cada uno | subtotal: ${subtotal:,.0f} COP"
                )

            print(f"Total a pagar: ${total:,.0f} COP")

            descuento = self.calcular_descuento()
            total_con_descuento = total - (total * descuento)

            if descuento > 0:
                print(f"Total con descuento: ${total_con_descuento:,.0f} COP")

            if descuento == 0.15:
                print("¡Felicidades! Has obtenido un descuento del 15% ")
            elif descuento == 0.3:
                print("¡Felicidades! Has obtenido un descuento del 30% ")
            else:
                print(
                    "No se ha aplicado ningún descuento. \n Para obtener descuentos, compra 3 o más unidades."
                )

    def realizar_compra(self, tienda: Tienda) -> None:
        """
        Permite confirmar la compra del carrito.

        :param tienda: Objeto de tipo Tienda.
        :return: None
        """
        if not self.items:
            print("El carrito se encuentra vacio. No se puede realizar la compra.")
            return

        self.mostrar_carrito()
        confirmacion = input("¿Desea confirmar la compra? (s/n): ").lower()
        if confirmacion != "s":
            print("Compra cancelada.")
            return
        else:
            print("Compra realizada con éxito. ¡Gracias por su compra!")
            self.vaciar_carrito()

    def calcular_descuento(self) -> float:
        """
        Calcula el porcentaje de descuento según
        la cantidad total de unidades en el carrito.

        - 5 o más unidades → 30%
        - 3 o más unidades → 15%
        - Menos de 3 → 0%

        :return: Porcentaje de descuento como float.
        """
        total_unidades = 0
        for codigo, item in self.items.items():
            total_unidades += item["cantidad"]

        if total_unidades >= 5:
            return 0.3
        elif total_unidades >= 3:
            return 0.15
        else:
            return 0
