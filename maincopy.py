import os
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox


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
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Orden', 'Fecha de búsqueda', 'Producto', 'Precio'])
        for index, producto in enumerate(data['productos'], start=1):
            writer.writerow(
                [index, data['fecha'], producto.nombre, producto.precio])


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
        return pd.DataFrame([(producto.nombre, producto.precio) for producto in self.productos], columns=["Producto", "Precio"])


def realizar_busqueda(producto, marca1, marca2, treeview1, treeview2):
    """
    Realiza la búsqueda de productos y muestra los resultados en dos tablas.

    Args:
        producto (str): El nombre del producto a buscar.
        marca1 (str): La primera marca a buscar.
        marca2 (str): La segunda marca a buscar.
        treeview1 (ttk.Treeview): El árbol para mostrar los productos de la marca 1.
        treeview2 (ttk.Treeview): El árbol para mostrar los productos de la marca 2.
    """
    terminos_busqueda = [
        (f"{producto} {marca1}", marca1),
        (f"{producto} {marca2}", marca2)
    ]

    treeview1.delete(*treeview1.get_children())
    treeview2.delete(*treeview2.get_children())

    for busqueda, marca in terminos_busqueda:
        busqueda_url = busqueda.strip().replace(" ", "-")
        url_busqueda = f'https://listado.mercadolibre.com.ar/{busqueda_url}#D[A:{busqueda.replace(" ", "%20")}]'

        buscador = BuscadorProductos(url_busqueda, marca, "")
        buscador.obtener_productos()

        for index, producto in enumerate(buscador.productos, start=1):
            if marca == marca1:
                treeview1.insert('', 'end', values=(
                    index, producto.nombre, producto.precio))
            else:
                treeview2.insert('', 'end', values=(
                    index, producto.nombre, producto.precio))

        # Guardar resultados en CSV para cada marca
        guardar_registro({'fecha': datetime.now().strftime(
            "%Y-%m-%d"), 'busqueda': busqueda_url, 'productos': buscador.productos}, marca)


def main():
    """
    Función principal que crea la interfaz gráfica y maneja la lógica de la aplicación.
    """
    root = tk.Tk()
    root.title("Comparador de Productos")

    # Estilo y tamaño de la fuente
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)

    # Creación de los widgets
    tk.Label(root, text="Producto:").grid(
        row=0, column=0, padx=10, pady=10, sticky="w")
    producto_entry = tk.Entry(root, width=30)
    producto_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    tk.Label(root, text="Marca 1:").grid(
        row=1, column=0, padx=10, pady=10, sticky="w")
    marca1_entry = tk.Entry(root, width=30)
    marca1_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    tk.Label(root, text="Marca 2:").grid(
        row=2, column=0, padx=10, pady=10, sticky="w")
    marca2_entry = tk.Entry(root, width=30)
    marca2_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    # Botón de búsqueda
    search_button = tk.Button(root, text="Buscar", command=lambda: on_buscar(
        producto_entry.get(), marca1_entry.get(), marca2_entry.get()), width=10)
    search_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    frame1 = tk.LabelFrame(root, text="Resultados Marca 1", padx=10, pady=10)
    frame1.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
    treeview1 = ttk.Treeview(frame1, columns=(
        "Orden", "Producto", "Precio"), show="headings")
    treeview1.heading("Orden", text="Orden", anchor="center")
    treeview1.heading("Producto", text="Producto", anchor="center")
    treeview1.heading("Precio", text="Precio", anchor="center")
    treeview1.column("Orden", width=50, anchor="center")
    treeview1.pack(fill=tk.BOTH, expand=True)

    frame2 = tk.LabelFrame(root, text="Resultados Marca 2", padx=10, pady=10)
    frame2.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
    treeview2 = ttk.Treeview(frame2, columns=(
        "Orden", "Producto", "Precio"), show="headings")
    treeview2.heading("Orden", text="Orden", anchor="center")
    treeview2.heading("Producto", text="Producto", anchor="center")
    treeview2.heading("Precio", text="Precio", anchor="center")
    treeview2.column("Orden", width=50, anchor="center")
    treeview2.pack(fill=tk.BOTH, expand=True)

    def on_buscar(producto, marca1, marca2):
        """
        Función que se ejecuta al hacer clic en el botón de buscar.
        """
        if producto and marca1 and marca2:
            realizar_busqueda(producto, marca1, marca2, treeview1, treeview2)
        else:
            messagebox.showwarning(
                "Entrada inválida", "Por favor ingrese el producto y ambas marcas.")

        # Actualizar textos de los frames con las marcas
        frame1.configure(text=f"Resultados Marca 1 - {marca1}")
        frame2.configure(text=f"Resultados Marca 2 - {marca2}")

    # Ajustar tamaño de los frames al expandir la ventana principal
    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
