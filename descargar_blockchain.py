import requests
import os

# --- 1. CONFIGURACIÓN ---
base_url = "https://api.blockchain.info/charts/"
# Parámetros para obtener todos los datos, en formato CSV
parametros = "?timespan=all&format=csv&sampled=false"

# Carpeta donde se guardarán los archivos
output_folder = 'datos_csv'

# Diccionario de los gráficos que queremos y cómo los llamaremos
charts_a_descargar = {
    'precio_btc': 'market-price',
    'hashrate_btc': 'hash-rate',
    'dificultad_btc': 'difficulty',
    'transacciones_btc': 'n-transactions',
    'ingresos_mineros_btc': 'miners-revenue'  # OJO: 'miners-revenue' es en BTC
}

# --- 2. CREAR CARPETAS ---
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Carpeta '{output_folder}' creada.")

print("Iniciando la descarga de los 5 datasets de Blockchain.com...")

# --- 3. BUCLE DE DESCARGA ---
for nombre_archivo, chart_name in charts_a_descargar.items():

    # Construir la URL completa
    url_completa = f"{base_url}{chart_name}{parametros}"

    print(f"\nDescargando {chart_name} ({nombre_archivo})...")
    print(f"URL: {url_completa}")

    try:
        # Hacer la petición GET a la API
        response = requests.get(url_completa)

        # Verificar si la petición fue exitosa (código 200)
        if response.status_code == 200:

            # Creamos el nombre completo del archivo
            file_path = os.path.join(output_folder, f"{nombre_archivo}.csv")

            # Escribir el contenido (que es el texto CSV) en el archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"¡Éxito! Datos guardados en: {file_path}")

        else:
            print(f"--- ERROR: La API devolvió un código {response.status_code} ---")

    except Exception as e:
        print(f"--- ERROR al descargar {chart_name} ---")
        print(f"Detalle: {e}")

print("\n--- Proceso de descarga de Bitcoin completado. ---")