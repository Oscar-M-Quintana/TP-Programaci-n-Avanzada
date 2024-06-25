import pandas as pd
import os
import matplotlib.pyplot as plt


def calcular_promedio_diario(marca):
    filename = f'registro_busquedas_{marca}.csv'
    if not os.path.isfile(filename):
        print(f"No se encontró el archivo: {filename}")
        return None

    df = pd.read_csv(filename, parse_dates=['Fecha de búsqueda'])

    # Calcular promedio diario de precios
    df['Fecha'] = df['Fecha de búsqueda'].dt.date
    promedio_diario = df.groupby('Fecha')['Precio'].mean().reset_index()

    # Guardar promedio diario en un nuevo archivo CSV
    promedio_diario.to_csv(f'promedio_diario_{marca}.csv', index=False)
    return promedio_diario


def graficar_variacion_precio(marca):
    filename = f'promedio_diario_{marca}.csv'
    if not os.path.isfile(filename):
        print(f"No se encontró el archivo: {filename}")
        return None

    df = pd.read_csv(filename, parse_dates=['Fecha'])

    plt.figure(figsize=(10, 6))
    plt.plot(df['Fecha'], df['Precio'], marker='o', linestyle='-', color='b')
    plt.title(f'Variación del Precio Promedio Diario - {marca}')
    plt.xlabel('Fecha')
    plt.ylabel('Precio Promedio')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f'variacion_precio_{marca}.png')
    plt.show()
