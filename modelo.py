# archivo: modelo.py

from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import csv


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
    Decorador para registrar las búsquedas de productos.

    Args:
        func (function): La función que realiza la búsqueda de productos.

    Returns:
        function: La función decorada que registra la búsqueda.
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
    Guarda un registro de la búsqueda en un archivo CSV.

    Args:
        data (dict): Un diccionario con los datos de la búsqueda.
        marca (str): La marca del producto buscado.
    """
    filename = f'{marca}.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Fecha de búsqueda', 'Producto', 'Precio'])
        for producto in data['productos']:
            writer.writerow([data['fecha'], producto.nombre, producto.precio])


class BuscadorProductos:
    """
    Clase que busca productos en una URL específica y registra los resultados.

    Attributes:
        url (str): La URL de búsqueda.
        marca (str): La marca del producto buscado.
        codigo (str): El código asociado a la búsqueda.
        productos (list): Una lista de productos encontrados.
    """

    def __init__(self, url, marca, codigo):
        self.url = url
        self.marca = marca
        self.codigo = codigo
        self.productos = []

    @registrar_busqueda
    def obtener_productos(self):
        """
        Obtiene productos de la URL y los almacena en la lista de productos.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            lista_productos = soup.find_all(
                'div', {'class': 'ui-search-result__content-wrapper'})
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
        Convierte la lista de productos a un DataFrame de pandas.

        Returns:
            DataFrame: Un DataFrame con los productos y sus precios.
        """
        import pandas as pd
        return pd.DataFrame([(producto.nombre, producto.precio) for producto in self.productos], columns=["Producto", "Precio"])
