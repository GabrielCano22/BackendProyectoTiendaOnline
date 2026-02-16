class Ropa:
    def __init__(self, tipo: str, marca: str, talla: str, color: str, precio: float):
        self.tipo = tipo
        self.marca = marca
        self.talla = talla
        self.color = color
        self.precio = precio

    def mostrar_informacion(self):
        print(f"Tipo: {self.tipo}")
        print(f"Marca: {self.marca}")
        print(f"Talla: {self.talla}")
        print(f"Color: {self.color}")
        print(f"Precio: ${self.precio}")


camisa = Ropa("Camisa", "Nike", "M", "Azul", 19.99)
camisa.mostrar_informacion()
