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
