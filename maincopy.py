import csv
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd


class Producto:
    """
    Clase que representa un producto con nombre y precio.

    Attributes:
        nombre (str): El nombre del producto.
        precio (str): El precio del producto.
    """

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre}: {self.precio}"


def registrar_busqueda(func):
    """
    Decorador para registrar la búsqueda de productos.

    Args:
        func (function): La función que se decora.

    Returns:
        function: La función decorada.
    """
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        busqueda = args[0]
        data = {
            'fecha': datetime.now().strftime("%Y-%m-%d"),
            'busqueda': busqueda.url,
            'productos': busqueda.productos,
            'codigo': busqueda.codigo
        }
        guardar_registro(data, busqueda.marca)
        return resultado
    return wrapper


def guardar_registro(data, marca):
    """
    Guarda el registro de búsqueda en un archivo CSV.

    Args:
        data (dict): Datos de la búsqueda.
        marca (str): Marca del producto.
    """
    filename = f'registro_busquedas_{marca}.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Fecha de búsqueda', 'Producto', 'Precio'])

        # Guardar los productos en el archivo CSV
        for producto in data['productos']:
            writer.writerow([data['fecha'], producto.nombre, producto.precio])


class BuscadorProductos:
    """
    Clase que realiza la búsqueda de productos en MercadoLibre.

    Attributes:
        url (str): URL de la búsqueda en MercadoLibre.
        marca (str): Marca del producto.
        codigo (str): Código del producto.
        productos (list): Lista de productos encontrados.
    """

    def __init__(self, url, marca, codigo):
        self.url = url
        self.marca = marca
        self.codigo = codigo
        self.productos = []

    @registrar_busqueda
    def obtener_productos(self):
        """
        Obtiene los productos de la página de búsqueda y los guarda en la lista de productos.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            lista_productos = soup.find_all(
                'div', {'class': 'ui-search-result__content-wrapper'})
            # Limitar la búsqueda a los primeros 20 productos
            for producto in lista_productos[:20]:
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
        """
        Convierte la lista de productos en un DataFrame de pandas.

        Returns:
            DataFrame: DataFrame con los productos y precios.
        """
        return pd.DataFrame([(producto.nombre, producto.precio) for producto in self.productos], columns=["Producto", "Precio"])


def main():
    """
    Función principal que realiza la búsqueda de productos y guarda los resultados.
    """

    solicitud_producto = input("Que producto desea comparar: ")
    solicitud_marca = input("Que marcas desea comparar: ")
    fin_solicitud = input("Desea agregar una marca mas?: (s/n)")

    terminos_busqueda = [
        ("Smart Tv 50 Pulgadas 4k Ultra Hd 50uq8050psb - LG", "LG", "50uq8050psb"),
        ("smart tv samsung 50 Un50cu7000 led 4k", "Samsung", "un50cu7000"),
        ("smart tv bgh google tv 5023us6g led 4k 50", "BGH", "5023us6g"),
        ("Smart Tv Noblex Dk50x6550pi Led Hdr 4k 50", "Noblex", "dk50x6550pi"),
        ("smart tv tcl L50c645 50 4k qled google tv hdr bidcom", "TCL", "l50c645")
    ]

    for busqueda, marca, codigo in terminos_busqueda:
        busqueda_url = busqueda.strip().replace(" ", "-")
        url_busqueda = f'https://listado.mercadolibre.com.ar/{busqueda_url}#D[A:{busqueda.replace(" ", "%20")}]'

        buscador = BuscadorProductos(url_busqueda, marca, codigo)
        buscador.obtener_productos()

        df = buscador.productos_a_dataframe()
        print(f"Productos encontrados para '{busqueda}':")
        print(df)

        print(f"\n{len(buscador.productos)} productos guardados en el registro.\n")


if __name__ == "__main__":
    main()
