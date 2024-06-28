# Comparador de Productos

Este proyecto es una aplicación en Python que busca productos en MercadoLibre y compara precios entre dos marcas diferentes. Utiliza una interfaz gráfica construida con Tkinter para facilitar la interacción con el usuario.

Integrantes del grupo:
- Rocío Palacios
- Oscar Quintana
- Nicolas Ozimuk

## Características

- **Búsqueda de productos**: Realiza búsquedas de productos en MercadoLibre especificando el nombre del producto y dos marcas.
- **Comparación de precios**: Compara los precios de los productos encontrados para las dos marcas especificadas.
- **Interfaz gráfica**: Interfaz amigable creada con Tkinter para ingresar datos y mostrar resultados.
- **Registro de búsqueda**: Guarda un registro de los resultados de la búsqueda en archivos CSV.

## Requisitos

- Python 3.x
- Paquetes necesarios: `requests`, `beautifulsoup4`, `tkinter`

Puedes instalar los paquetes necesarios usando pip:

```bash
pip install requests beautifulsoup4
```

## Uso
1. Clona este repositorio o descarga los archivos.
2. Ejecuta el archivo principal main.py.
3. Introduce el nombre del producto y las dos marcas que deseas comparar.
4. Haz clic en el botón "Buscar" para realizar la búsqueda y mostrar los resultados.

## Estructura del proyecto
- `Producto`: Clase que representa un producto con nombre y precio.
- `BuscadorProductos`: Clase que busca productos en una URL específica y registra los resultados.
- `InterfazGrafica`: Clase que maneja la interfaz gráfica de la aplicación.







