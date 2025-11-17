import pandas as pd
import os
import sys
import traceback

# --- CONFIGURACIÓN ---
CARPETA_DATOS = "datos_csv"
FECHA_INICIO = "2011-01-01"  # <--- Nueva constante para definir el corte

FILES = {
    "price": "precio_btc.csv",
    "hashrate": "hashrate_btc.csv",
    "difficulty": "dificultad_btc.csv",
    "transactions": "transacciones_btc.csv",
    "reward": "ingresos_mineros_btc.csv",  # Contiene USD
    "eia": "Average_retail_price_of_electricity_monthly.csv",
    "efficiency": "efficiency_manual.csv"
}
PATHS = {k: os.path.join(CARPETA_DATOS, v) for k, v in FILES.items()}


# --- FUNCIONES AUXILIARES ---

def parse_eia_date(date_str):
    if pd.isna(date_str) or str(date_str).strip() == '': return pd.NaT
    date_str = str(date_str).strip()
    try:
        return pd.to_datetime(date_str, format='%b-%y')
    except:
        pass
    try:
        return pd.to_datetime(date_str, format='%b %Y')
    except:
        pass
    try:
        return pd.to_datetime(date_str)
    except:
        return pd.NaT


# --- CARGA DE DATOS ---

def load_blockchain_data(paths):
    print("\n--- 1. Procesando Blockchain.com ---")
    dfs = []

    metrics_map = {
        "price": "price_usd",
        "hashrate": "hashrate_th_s",
        "difficulty": "difficulty",
        "transactions": "transactions_count",
        "reward": "miners_revenue_usd"
    }

    for key, col_name in metrics_map.items():
        path = paths.get(key)
        if not os.path.exists(path):
            print(f"  ❌ FALTA: {path}")
            continue

        try:
            try:
                df = pd.read_csv(path, header=0, names=["date", col_name])
                pd.to_datetime(df.iloc[0, 0])
            except:
                df = pd.read_csv(path, header=None, names=["date", col_name])

            df["date"] = pd.to_datetime(df["date"])
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
            df.set_index("date", inplace=True)
            df = df[~df.index.duplicated(keep='first')]
            dfs.append(df)
            print(f"  ✅ {key}: {len(df)} registros")
        except Exception as e:
            print(f"  ❌ Error leyendo {key}: {e}")

    if not dfs: return None

    print("  -> Uniendo datasets...")
    df_base = dfs[0]
    for df in dfs[1:]:
        df_base = df_base.join(df, how='outer')

    df_base = df_base.interpolate(method='time')
    return df_base


def load_eia_data(file_path):
    print(f"\n--- 2. Procesando EIA (Electricidad) ---")
    if not os.path.exists(file_path):
        print(f"  ❌ No encontrado: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path, sep=';', header=4, engine='python')
        df.columns = [c.strip() for c in df.columns]

        col_date = 'Month'
        col_price = next((c for c in df.columns if 'industrial' in c.lower()), None)

        if not col_price:
            print("  ⚠️ No se encontró columna 'industrial'")
            return None

        df = df.rename(columns={col_date: 'date', col_price: 'price_cents'})
        df = df[['date', 'price_cents']].dropna()
        df['price_cents'] = pd.to_numeric(df['price_cents'], errors='coerce')

        df['date'] = df['date'].apply(parse_eia_date)
        df = df.dropna(subset=['date']).set_index('date').sort_index()

        df['electricity_price_usd_kwh'] = df['price_cents'] / 100
        df_daily = df.resample('D').ffill()

        print(f"  ✅ EIA cargado: {len(df_daily)} días generados.")
        return df_daily[['electricity_price_usd_kwh']]

    except Exception as e:
        print(f"  ❌ Error EIA: {e}")
        return None


def load_efficiency_data(file_path):
    print(f"\n--- 3. Procesando Eficiencia ---")
    if not os.path.exists(file_path):
        print(f"  ❌ No encontrado: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path, sep=None, engine='python', dtype=str)
        df.columns = [c.strip().lower() for c in df.columns]

        col_map = {
            'fecha': 'date', 'date': 'date',
            'efficiency': 'efficiency_j_th', 'eficiencia': 'efficiency_j_th', 'efficiency_j_th': 'efficiency_j_th'
        }
        df = df.rename(columns=col_map)

        if 'date' not in df.columns:
            df.columns = ['date', 'efficiency_j_th']

        df['efficiency_j_th'] = df['efficiency_j_th'].str.replace(',', '.', regex=False)
        df['efficiency_j_th'] = pd.to_numeric(df['efficiency_j_th'], errors='coerce')

        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

        df = df.dropna(subset=['date', 'efficiency_j_th']).set_index('date').sort_index()

        df_daily = df.resample('D').ffill()

        print(f"  ✅ Eficiencia cargada: {len(df_daily)} días generados.")
        return df_daily

    except Exception as e:
        print(f"  ❌ Error Eficiencia Detallado:")
        traceback.print_exc()
        return None


# --- MAIN ---

if __name__ == "__main__":
    df_btc = load_blockchain_data(PATHS)
    df_elec = load_eia_data(PATHS["eia"])
    df_eff = load_efficiency_data(PATHS["efficiency"])

    print("\n--- 4. Unificación Final ---")
    if df_btc is not None:
        df_master = df_btc
        if df_elec is not None: df_master = df_master.join(df_elec, how='left')
        if df_eff is not None: df_master = df_master.join(df_eff, how='left')

        df_master = df_master.ffill()

        # --- CÁLCULO COLUMNA DERIVADA (Ingresos en BTC) ---
        if 'miners_revenue_usd' in df_master.columns and 'price_usd' in df_master.columns:
            print("  -> Calculando miners_revenue_btc...")
            df_master['miners_revenue_btc'] = df_master.apply(
                lambda row: row['miners_revenue_usd'] / row['price_usd'] if row['price_usd'] > 0 else 0,
                axis=1
            )

        # --- FILTRADO POR FECHA (Nuevo) ---
        print(f"  -> Recortando dataset desde {FECHA_INICIO}...")
        df_master = df_master[df_master.index >= FECHA_INICIO]

        output_file = "dataset_completo_bitcoin.csv"
        df_master.to_csv(output_file)
        print(f"🎉 ¡PROCESO TERMINADO! Guardado en: {output_file}")
        print(f"Dimensiones Finales: {df_master.shape}")
        print(df_master[['price_usd', 'miners_revenue_usd', 'miners_revenue_btc']].head())
    else:
        print("❌ No se pudo generar el dataset base.")