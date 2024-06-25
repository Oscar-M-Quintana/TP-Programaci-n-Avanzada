import requests
from bs4 import BeautifulSoup
import pandas as pd


class Libro:
    def __init__(self, titulo, autor, precio, disponibilidad):
        self.titulo = titulo
        self.autor = autor
        self.precio = precio
        self.disponibilidad = disponibilidad

    def __str__(self):
        return f"{self.titulo} por {self.autor} - {self.precio} ({self.disponibilidad})"


class BuscadorLibros:
    def __init__(self, url):
        self.url = url
        self.libros = []

    def obtener_libros(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            lista_libros = soup.find_all('article', class_='product_pod')
            for libro in lista_libros:
                try:
                    titulo = libro.h3.a['title']
                    autor = libro.find('h3').text.strip()
                    precio = libro.find('p', class_='price_color').text.strip()
                    disponibilidad = libro.find(
                        'p', class_='instock availability').text.strip()
                    self.libros.append(
                        Libro(titulo, autor, precio, disponibilidad))
                except AttributeError as e:
                    print(f"Error al procesar el libro: {e}")
                    continue
        else:
            print(f"Error al acceder a la URL: {response.status_code}")

    def libros_a_dataframe(self):
        return pd.DataFrame([(libro.titulo, libro.autor, libro.precio, libro.disponibilidad) for libro in self.libros],
                            columns=["Título", "Autor", "Precio", "Disponibilidad"])


def main():
    url = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'
    buscador = BuscadorLibros(url)
    buscador.obtener_libros()

    df = buscador.libros_a_dataframe()
    print("Libros encontrados:")
    print(df)

    # Guardar los datos en un archivo CSV
    df.to_csv('libros.csv', index=False, encoding='utf-8-sig')
    print("\nDatos guardados en 'libros.csv'")


if __name__ == "__main__":
    main()
