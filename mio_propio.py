import csv
import os
import random
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = "https://www.carrefour.com.ar/Bebidas/Vinos?order="

try:
    # Tiempo de espera establecido en 5 segundos
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Genera una excepción para errores HTTP
except requests.exceptions.Timeout:
    print("La solicitud ha superado el tiempo de espera")
except requests.exceptions.RequestException as e:
    print(f"Ha ocurrido un error: {e}")

soup_html = BeautifulSoup(response.content, 'html.parser')
soup_html5 = BeautifulSoup(response.content, 'html.parser')
soup_lxlm = BeautifulSoup(response.content, 'html.parser')

for string in soup_html.stripped_strings:
    print(repr(string))

clase_buscada = soup_html.find_all(
    "span", class_="jumboargentinaio-store-theme-1QiyQadHj-1_x9js9EXUYK")
print(clase_buscada)

"""         if response.status_code == 200:
            lista_productos = soup.find_all(
                'div', {'class': 'ui-search-result__content-wrapper'})
            # Limitar la búsqueda a los primeros 20 productos
            for idx, producto in enumerate(lista_productos[:20], start=1):
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
        else:
            print(f"Error al acceder a la URL: {response.status_code}")

    def productos_a_dataframe(self):
        return pd.DataFrame([(producto.nombre, producto.precio) for producto in self.productos], columns=["Producto", "Precio"])
"""

""" def main():
    terminos_busqueda = [
        ("Smart Tv 50 Pulgadas 4k Ultra Hd 50uq8050psb - LG", "LG", "50uq8050psb"),
        ("smart tv samsung 50 Un50cu7000 led 4k", "Samsung", "un50cu7000"),
        ("smart tv bgh google tv 5023us6g led 4k 50", "BGH", "5023us6g"),
        ("Smart Tv Noblex Dk50x6550pi Led Hdr 4k 50", "Noblex", "dk50x6550pi"),
        ("smart tv tcl L50c645 50 4k qled google tv hdr bidcom", "TCL", "l50c645")
    ]

    for busqueda, marca, codigo in terminos_busqueda:

        buscador = BuscadorProductos(url_busqueda, marca, codigo)
        buscador.obtener_productos()

        df = buscador.productos_a_dataframe()
        print(f"Productos encontrados para '{busqueda}':")
        print(df)

        print(f"\n{len(buscador.productos)} productos guardados en el registro.\n") """
