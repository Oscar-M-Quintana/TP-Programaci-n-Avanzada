import requests
from bs4 import BeautifulSoup
import pandas as pd


class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre}: {self.precio}"


class BuscadorProductos:
    def __init__(self, url):
        self.url = url
        self.productos = []

    def obtener_productos(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to load page {self.url}")

        soup = BeautifulSoup(response.content, 'html.parser')
        lista_productos = soup.find_all(
            'li', {'class': 'ui-search-layout__item'})

        for producto in lista_productos:
            try:
                nombre = producto.find(
                    'h2', {'class': 'ui-search-item__title'})
                nombre = nombre.text.strip() if nombre else "No disponible"

                simbolo_moneda = producto.find(
                    'span', {'class': 'andes-money-amount__currency-symbol'})
                simbolo_moneda = simbolo_moneda.text.strip() if simbolo_moneda else "$"

                precio = producto.find(
                    'span', {'class': 'andes-money-amount__fraction'})
                precio = simbolo_moneda + precio.text.strip() if precio else "No disponible"

                self.productos.append(Producto(nombre, precio))
            except AttributeError as e:
                print(f"Error al procesar el producto: {e}")
                continue

    def productos_a_dataframe(self):
        return pd.DataFrame([(producto.nombre, producto.precio) for producto in self.productos], columns=["Producto", "Precio"])

    def generar_mensaje_whatsapp(self):
        mensaje = "Productos encontrados:\n\n"
        for producto in self.productos:
            mensaje += f"{producto}\n"
        return mensaje


def main():
    busqueda = input("¿Qué estás buscando? ")
    url_busqueda = f'https://listado.mercadolibre.com.ar/{busqueda}#D[A:{busqueda}]'

    buscador = BuscadorProductos(url_busqueda)
    buscador.obtener_productos()

    df = buscador.productos_a_dataframe()
    print(df)

    mensaje = buscador.generar_mensaje_whatsapp()
    print("\nMensaje para enviar por WhatsApp:")
    print(mensaje)


if __name__ == "__main__":
    main()
