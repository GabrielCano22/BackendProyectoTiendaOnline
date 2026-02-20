class Carrito:
    def __init__(self):
        self.items = {}

    def agregar_producto(self, tienda, codigo, cantidad):

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

    def vaciar_carrito(self):
        self.items = {}

    def mostrar_carrito(self):
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

    def realizar_compra(self, tienda):
        if not self.items:
            print("El carrito se encuentra vacio. No se puede realizar la compra.")
            return

        self.mostrar_carrito()
        comfirmacion = input("¿Desea confirmar la compra? (s/n): ").lower()
        if comfirmacion != "s":
            print("Compra cancelada.")
            return
        else:
            print("Compra realizada con éxito. ¡Gracias por su compra!")
            self.vaciar_carrito()
