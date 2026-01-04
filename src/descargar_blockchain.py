import requests
import os

# --- 1. CONFIGURACIÓN ---
base_url = "https://api.blockchain.info/charts/"
parametros = "?timespan=all&format=csv&sampled=false"
output_folder = 'datos/raw_api'

# Diccionario mapeando: nombre_archivo -> endpoint_api
charts_a_descargar = {
    # --- Mercado y Valor ---
    'precio_btc': 'market-price',
    'market_cap': 'market-cap',
    'trade_volume_exchange': 'trade-volume',  # Volumen en Exchanges (aprox)

    # --- Minería y Seguridad ---
    'hashrate': 'hash-rate',
    'dificultad': 'difficulty',
    'miners_revenue_usd': 'miners-revenue',  # Ingresos totales en USD

    # --- Uso de la Red (Bloques y Transacciones) ---
    'transacciones_dia': 'n-transactions',
    'transacciones_segundo': 'transactions-per-second',
    'mempool_size': 'mempool-size',  # Congestión de la red (bytes)
    'avg_block_size': 'avg-block-size',  # Tamaño promedio de bloque
    'n_unique_addresses': 'n-unique-addresses',  # Direcciones únicas usadas
    'total_btc_sent': 'total-bitcoins',  # BTC totales en circulación

    # --- Costes (Fees) ---
    'fees_total_btc': 'transaction-fees',  # Fees totales pagados a mineros en BTC
    'cost_per_tx': 'cost-per-transaction'  # Coste por transacción minada
}

def main():
    # --- 2. CREAR CARPETAS ---
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Carpeta '{output_folder}' creada/verificada.")

    print(f"Iniciando descarga de {len(charts_a_descargar)} datasets de Blockchain.com...")

    # --- 3. BUCLE DE DESCARGA ---
    for nombre_archivo, chart_name in charts_a_descargar.items():
        url_completa = f"{base_url}{chart_name}{parametros}"
        print(f"Descargando: {nombre_archivo} ({chart_name})...")

        try:
            response = requests.get(url_completa)
            if response.status_code == 200:
                file_path = os.path.join(output_folder, f"{nombre_archivo}.csv")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
            else:
                print(f"  ERROR {response.status_code} en {chart_name}")
        except Exception as e:
            print(f"  ERROR EXCEPCIÓN en {chart_name}: {e}")

    print("\n--- Descarga masiva completada. ---")

if __name__ == "__main__":
    main()