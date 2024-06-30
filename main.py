import csv
import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime
from tkinter import messagebox, ttk
from tkinter import Canvas
import requests
from bs4 import BeautifulSoup


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


class BuscadorProductos:
    """
    Clase que busca productos en una URL específica y registra los resultados.

    Attributes:
        url (str): La URL de búsqueda.
        marca (str): La marca del producto buscado.
        productos (list): Una lista de productos encontrados.
    """

    def __init__(self, url, marca, archivo_csv):
        self.url = url
        self.marca = marca
        self.productos = []
        self.archivo_csv = archivo_csv

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

                    # Verificar si el nombre del producto contiene la marca
                    if self.marca.lower() in nombre.lower():
                        self.productos.append(Producto(nombre, precio))
                except AttributeError as e:
                    print(f"Error al procesar el producto: {e}")
                    continue
        else:
            print(f"Error al acceder a la URL: {response.status_code}")

    def guardar_registro(self):
        """
        Guarda un registro de la búsqueda en un archivo CSV.
        """
        with open(self.archivo_csv, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Orden', 'Fecha de búsqueda', 'Producto', 'Precio'])
            for index, producto in enumerate(self.productos, start=1):
                writer.writerow([index, datetime.now().strftime(
                    "%Y-%m-%d"), producto.nombre, producto.precio])

    @staticmethod
    def construir_url(producto, marca):
        """
        Construye la URL de búsqueda basada en el producto y la marca.

        Args:
            producto (str): El nombre del producto a buscar.
            marca (str): La marca del producto a buscar.

        Returns:
            str: La URL completa de búsqueda.
        """
        busqueda_url = f'{producto}-{marca}'.replace(" ", "-")
        return f'https://listado.mercadolibre.com.ar/{busqueda_url}#D[A:{producto.replace(" ", "%20")}]'


class InterfazGrafica:
    """
    Clase que maneja la interfaz gráfica de la aplicación.

    Attributes:
        root (tk.Tk): La ventana principal de tkinter.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Scrapify")

        # Estilo y tamaño de la fuente
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.root.option_add("*Font", default_font)

        # Estilo del título
        title_font = tkFont.Font(family="Helvetica", size=28, weight="bold")
        canvas = Canvas(self.root, width=300, height=100,
                        bg=self.root.cget('bg'), highlightthickness=0)
        canvas.grid(row=0, column=0, columnspan=2,
                    padx=20, pady=(20, 0), sticky="n")
        x, y = 150, 50
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            canvas.create_text(x + dx, y + dy, text="Scrapify",
                               font=title_font, fill="black")
        canvas.create_text(x, y, text="Scrapify", font=title_font, fill="blue")

        # Creación de los widgets
        tk.Label(self.root, text="Producto:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.producto_entry = tk.Entry(self.root, width=30)
        self.producto_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.root, text="Marca 1:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        self.marca1_entry = tk.Entry(self.root, width=30)
        self.marca1_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.root, text="Marca 2:").grid(
            row=3, column=0, padx=10, pady=10, sticky="w")
        self.marca2_entry = tk.Entry(self.root, width=30)
        self.marca2_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Botón de búsqueda
        search_button = tk.Button(
            self.root, text="Buscar", command=self.on_buscar, width=10)
        search_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.frame1 = tk.LabelFrame(
            self.root, text="Resultados Marca 1", padx=10, pady=10)
        self.frame1.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        self.treeview1 = ttk.Treeview(self.frame1, columns=(
            "Orden", "Producto", "Precio"), show="headings")
        self.treeview1.heading("Orden", text="Orden", anchor="center")
        self.treeview1.heading("Producto", text="Producto", anchor="center")
        self.treeview1.heading("Precio", text="Precio", anchor="center")
        self.treeview1.column("Orden", width=50, anchor="center")
        self.treeview1.pack(fill=tk.BOTH, expand=True)

        self.frame2 = tk.LabelFrame(
            self.root, text="Resultados Marca 2", padx=10, pady=10)
        self.frame2.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")
        self.treeview2 = ttk.Treeview(self.frame2, columns=(
            "Orden", "Producto", "Precio"), show="headings")
        self.treeview2.heading("Orden", text="Orden", anchor="center")
        self.treeview2.heading("Producto", text="Producto", anchor="center")
        self.treeview2.heading("Precio", text="Precio", anchor="center")
        self.treeview2.column("Orden", width=50, anchor="center")
        self.treeview2.pack(fill=tk.BOTH, expand=True)

        # Ajustar tamaño de los frames al expandir la ventana principal
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Pie de página
        footer_font = tkFont.Font(size=8)
        tk.Label(self.root, text="Created by: Nicolas Ozimuk, Oscar Quintana y Rocío Palacios", font=footer_font).grid(
            row=6, column=0, columnspan=2, pady=(0, 10), sticky="s")

    def on_buscar(self):
        """
        Función que se ejecuta al hacer clic en el botón de buscar.
        """
        producto = self.producto_entry.get()
        marca1 = self.marca1_entry.get()
        marca2 = self.marca2_entry.get()
        if producto and marca1 and marca2:
            url1 = BuscadorProductos.construir_url(producto, marca1)
            url2 = BuscadorProductos.construir_url(producto, marca2)
            buscador1 = BuscadorProductos(url1, marca1, 'marca1.csv')
            buscador2 = BuscadorProductos(url2, marca2, 'marca2.csv')
            buscador1.obtener_productos()
            buscador2.obtener_productos()
            self.mostrar_resultados(buscador1, buscador2)
            buscador1.guardar_registro()
            buscador2.guardar_registro()
        else:
            messagebox.showwarning(
                "Entrada inválida", "Por favor ingrese el producto y ambas marcas.")

    def mostrar_resultados(self, buscador1, buscador2):
        """
        Muestra los resultados de la búsqueda en los Treeviews.
        """
        for i in self.treeview1.get_children():
            self.treeview1.delete(i)
        for i in self.treeview2.get_children():
            self.treeview2.delete(i)

        for index, producto in enumerate(buscador1.productos, start=1):
            self.treeview1.insert("", "end", values=(
                index, producto.nombre, producto.precio))

        for index, producto in enumerate(buscador2.productos, start=1):
            self.treeview2.insert("", "end", values=(
                index, producto.nombre, producto.precio))


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()
