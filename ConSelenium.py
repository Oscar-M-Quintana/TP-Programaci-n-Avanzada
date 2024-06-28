from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import pandas as pd

# Configuración de las opciones de Chrome
chrome_options = Options()
# Ejecutar en modo headless (sin interfaz gráfica)
chrome_options.add_argument("--headless")

# Inicializar el driver de Chrome
driver = webdriver.Chrome(options=chrome_options)

# URL de la página a scrapear
url = "https://www.carrefour.es/supermercado"

# Cargar la página en el driver de Selenium
driver.get(url)

# Esperar a que la página cargue completamente (puedes ajustar el tiempo de espera según sea necesario)
driver.implicitly_wait(10)  # Esperar hasta 10 segundos

# Obtener el HTML de la página cargada
html = driver.page_source

# Parsear el contenido HTML con BeautifulSoup
soup = bs(html, 'html.parser')

# Encontrar todos los productos
productos = soup.find_all('div', class_='product-card__parent')

# Mostrar todo el html
print(soup.prettify())

# Crear listas para almacenar los datos de los productos
nombres = []
precios = []

# Extraer información de cada producto
for producto in productos:
    try:
        nombre_producto = producto.find(
            'h2', class_='product-card__title').text.strip()
        precio_producto = producto.find(
            'span', class_='product-card__price').text.strip()

        nombres.append(nombre_producto)
        precios.append(precio_producto)
    except AttributeError as e:
        print(f"Error al procesar el producto: {e}")
        continue

# Crear un DataFrame con los datos obtenidos
df = pd.DataFrame({
    'Nombre': nombres,
    'Precio': precios
})

# Guardar los datos en un archivo CSV
df.to_csv('productos_carrefour.csv', index=False, encoding='utf-8-sig')

# Cerrar el driver de Selenium
driver.quit()

print("Scraping completado. Los datos se han guardado en 'productos_carrefour.csv'.")
