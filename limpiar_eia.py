import pandas as pd
import os

# CONFIGURACIÓN
INPUT_FILE = os.path.join("datos_csv", "Average_retail_price_of_electricity_monthly.csv")
OUTPUT_FILE = os.path.join("datos_csv", "eia_limpio.csv")


def limpiar_eia():
    print("🧹 Limpiando archivo EIA...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ No encuentro el archivo: {INPUT_FILE}")
        return

    # 1. Leer el archivo con la configuración EXACTA
    try:
        # skiprows=4: Salta las líneas de título/metadatos
        # sep=';': El separador de columnas que me has confirmado
        # decimal='.': El separador decimal que me has confirmado
        df = pd.read_csv(INPUT_FILE, skiprows=4, header=0, names=['Month', 'Price'], sep=';', decimal='.')

        print("  -> Archivo leído correctamente. Primeras filas:")
        print(df.head(2))

    except Exception as e:
        print(f"❌ Error crítico leyendo CSV: {e}")
        return

    # 2. Limpieza de filas vacías
    df = df.dropna(how='all')
    # Filtramos filas donde 'Month' sea demasiado corto (basura)
    df = df[df['Month'].astype(str).str.len() > 3]

    # 3. Normalización de Fechas (Manejo de formatos mixtos)
    def parse_mixed_dates(date_str):
        date_str = str(date_str).strip()
        try:
            return pd.to_datetime(date_str, format='%b-%y')  # Ej: jul-25
        except:
            pass
        try:
            return pd.to_datetime(date_str, format='%b %Y')  # Ej: Apr 2025
        except:
            return pd.NaT

    df['date'] = df['Month'].apply(parse_mixed_dates)

    # 4. Limpieza de Precio
    # Aseguramos que sea numérico (aunque con decimal='.' ya debería serlo)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Ajuste de unidades: La EIA suele dar datos en CENTAVOS.
    # Si el precio es > 1 (ej. 8.21), asumimos centavos y convertimos a dólares.
    mask_cents = df['Price'] > 1
    df.loc[mask_cents, 'Price'] = df.loc[mask_cents, 'Price'] / 100

    # 5. Guardar archivo limpio (formato estándar comas para el siguiente paso)
    df_final = df[['date', 'Price']].dropna().sort_values('date')
    df_final.columns = ['date', 'elec_cost_kwh']

    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Archivo limpio generado: {OUTPUT_FILE}")
    print(df_final.head())


if __name__ == "__main__":
    limpiar_eia()