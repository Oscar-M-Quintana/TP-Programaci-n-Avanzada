# Buscador de Productos

Este proyecto es una aplicación en Python que busca productos en MercadoLibre a partir de términos de búsqueda específicos. Los resultados se registran en un archivo CSV para su posterior análisis.

## Descripción

La aplicación realiza las siguientes funciones:
1. **Busca productos** en MercadoLibre utilizando términos de búsqueda específicos.
2. **Extrae información** sobre los productos, como el nombre y el precio.
3. **Registra los resultados** de la búsqueda en un archivo CSV.
4. **Genera datos** para los últimos 15 días con precios aleatorios para los productos encontrados.

## Estructura del Proyecto

- `Producto`: Clase que representa un producto con un nombre y un precio.
- `registrar_busqueda`: Decorador que registra la búsqueda y los productos encontrados.
- `guardar_registro`: Función que guarda los resultados de la búsqueda en un archivo CSV.
- `BuscadorProductos`: Clase que realiza la búsqueda de productos en MercadoLibre.
- `main`: Función principal que realiza búsquedas para varios términos y guarda los resultados.

## Requisitos

- Python 3.x
- Librerías: `requests`, `beautifulsoup4`, `pandas`

Puedes instalar las librerías necesarias ejecutando:

```sh
pip install requests beautifulsoup4 pandas

## Uso

1. Clona este repositorio:
git clone https://github.com/tu_usuario/buscador_productos.git

2. Navega al directorio del proyecto:
cd buscador_productos

3. Ejecuta el script principal:
python main.py

El script buscará productos en MercadoLibre para los términos especificados, mostrará los productos encontrados en la consola y guardará los resultados en un archivo CSV con el nombre registro_busquedas_{marca}.csv.

## Personalización
Puedes personalizar los términos de búsqueda y las marcas en la lista terminos_busqueda en la función main:
terminos_busqueda = [
    ("Smart Tv 50 Pulgadas 4k Ultra Hd 50uq8050psb - LG", "LG", "50uq8050psb"),
    ("smart tv samsung 50 Un50cu7000 led 4k", "Samsung", "un50cu7000"),
    ("smart tv bgh google tv 5023us6g led 4k 50", "BGH", "5023us6g"),
    ("Smart Tv Noblex Dk50x6550pi Led Hdr 4k 50", "Noblex", "dk50x6550pi"),
    ("smart tv tcl L50c645 50 4k qled google tv hdr bidcom", "TCL", "l50c645")
]

