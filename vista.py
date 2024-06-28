import tkinter as tk
from tkinter import ttk, messagebox
from modelo import BuscadorProductos


class Vista(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comparador de Productos")
        self.geometry("800x600")

        # Definir widgets
        self.producto_label = tk.Label(self, text="Producto:")
        self.producto_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.producto_entry = tk.Entry(self, width=30)
        self.producto_entry.grid(
            row=0, column=1, padx=10, pady=10, sticky="ew")

        self.marca1_label = tk.Label(self, text="Marca 1:")
        self.marca1_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.marca1_entry = tk.Entry(self, width=30)
        self.marca1_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.marca2_label = tk.Label(self, text="Marca 2:")
        self.marca2_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.marca2_entry = tk.Entry(self, width=30)
        self.marca2_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.search_button = tk.Button(
            self, text="Buscar", command=self.on_buscar, width=10)
        self.search_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.frame1 = tk.LabelFrame(
            self, text="Resultados Marca 1", padx=10, pady=10)
        self.frame1.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.treeview1 = ttk.Treeview(self.frame1, columns=(
            "Orden", "Producto", "Precio"), show="headings")
        self.treeview1.heading("Orden", text="Orden", anchor="center")
        self.treeview1.heading("Producto", text="Producto", anchor="center")
        self.treeview1.heading("Precio", text="Precio", anchor="center")
        self.treeview1.column("Orden", width=50, anchor="center")
        self.treeview1.pack(fill=tk.BOTH, expand=True)

        self.frame2 = tk.LabelFrame(
            self, text="Resultados Marca 2", padx=10, pady=10)
        self.frame2.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
        self.treeview2 = ttk.Treeview(self.frame2, columns=(
            "Orden", "Producto", "Precio"), show="headings")
        self.treeview2.heading("Orden", text="Orden", anchor="center")
        self.treeview2.heading("Producto", text="Producto", anchor="center")
        self.treeview2.heading("Precio", text="Precio", anchor="center")
        self.treeview2.column("Orden", width=50, anchor="center")
        self.treeview2.pack(fill=tk.BOTH, expand=True)

    def on_buscar(self):
        producto = self.producto_entry.get()
        marca1 = self.marca1_entry.get()
        marca2 = self.marca2_entry.get()

        if producto and marca1 and marca2:
            self.realizar_busqueda(producto, marca1, marca2)
        else:
            messagebox.showwarning(
                "Entrada inválida", "Por favor ingrese el producto y ambas marcas.")

    def realizar_busqueda(self, producto, marca1, marca2):
        # Instanciar el buscador con datos ficticios
        buscador = BuscadorProductos('', '', '')
        # Simulación de búsqueda
        productos_marca1 = [(1, "Producto A", "$10.00"),
                            (2, "Producto B", "$15.00")]
        productos_marca2 = [(1, "Producto C", "$12.00"),
                            (2, "Producto D", "$18.00")]

        # Llenar treeview con datos simulados
        self.llenar_treeview(self.treeview1, productos_marca1)
        self.llenar_treeview(self.treeview2, productos_marca2)

    def llenar_treeview(self, treeview, data):
        treeview.delete(*treeview.get_children())
        for item in data:
            treeview.insert('', 'end', values=item)


if __name__ == "__main__":
    app = Vista()
    app.mainloop()
