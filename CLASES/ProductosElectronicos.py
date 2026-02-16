class ProductosElectronicos:
    def __init__(self, marca, modelo, precio):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio

    def mostrar_informacion(self):
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Precio: ${self.precio}")

Producto1 = ProductosElectronicos("Apple", "iPhone 13", 999)
Producto1.mostrar_informacion()