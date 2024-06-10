import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv
import os


class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre}: {self.precio}"


def registrar_busqueda(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        busqueda = args[0]
        productos = [str(producto) for producto in busqueda.productos]
        data = {
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'busqueda': busqueda.url,
            'productos': busqueda.productos  # Guardar los objetos Producto directamente
        }
        guardar_registro(data)
        return resultado
    return wrapper


def guardar_registro(data):
    file_exists = os.path.isfile('registro_busquedas.csv')
    with open('registro_busquedas.csv', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Escribir título de referencia si el archivo no existe
            writer.writerow(['Registros de Búsquedas'])

        # Escribir los datos en celdas diferentes
        writer.writerow(['Fecha de búsqueda', 'Producto'])
        writer.writerow([data['fecha'], data['busqueda']])

        # Escribir los productos en celdas diferentes con cabecera
        writer.writerow(['Número de Orden', 'Producto', 'Precio'])
        for idx, producto in enumerate(data['productos'], start=1):
            writer.writerow([idx, producto.nombre, producto.precio])

        # Añadir línea vacía para separar búsquedas
        writer.writerow([])


class BuscadorProductos:
    def __init__(self, url):
        self.url = url
        self.productos = []

    @registrar_busqueda
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
        return pd.DataFrame(
            [(producto.nombre, producto.precio)
             for producto in self.productos],
            columns=["Producto", "Precio"]
        )

    def generar_mensaje_whatsapp(self):
        mensaje = "Productos encontrados:\n\n"
        for producto in self.productos:
            mensaje += f"{producto}\n"
        return mensaje


def main():
    busqueda = input("¿Qué estás buscando? ")
    busqueda_url = busqueda.replace(" ", "-")
    url_busqueda = f'https://listado.mercadolibre.com.ar/{busqueda_url}#D[A:{busqueda.replace(" ", "%20")}]'

    buscador = BuscadorProductos(url_busqueda)
    buscador.obtener_productos()

    df = buscador.productos_a_dataframe()
    print("hola")
    print(df)
    print("chau")

    mensaje = buscador.generar_mensaje_whatsapp()
    print("\nMensaje para enviar por WhatsApp:")
    print(mensaje)


if __name__ == "__main__":
    main()
