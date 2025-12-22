import pandas as pd
import os
import numpy as np
import warnings

# --- CONFIGURACIÓN ---
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('future.no_silent_downcasting', True)

CARPETA_DATOS = "datos_csv"
FECHA_INICIO = "2015-01-01"
OUTPUT_FILE = "dataset_final_btc_ampliado.csv"

# Archivos
FILE_EIA_CLEAN = "eia_limpio.csv"  # Usaremos el limpio
FILE_EFFICIENCY = "efficiency_manual.csv"


# --- 1. CARGA DE DATOS BLOCKCHAIN ---
def load_blockchain_files():
    print("--- 1. Cargando datos de Blockchain.com ---")
    dfs = []
    # Ignoramos manuales y outputs
    ignored = [FILE_EFFICIENCY, FILE_EIA_CLEAN, OUTPUT_FILE, "Average_retail_price_of_electricity_monthly.csv"]

    csv_files = [f for f in os.listdir(CARPETA_DATOS) if f.endswith('.csv') and f not in ignored]

    for file_name in csv_files:
        path = os.path.join(CARPETA_DATOS, file_name)
        col_name = file_name.replace('.csv', '')
        try:
            try:
                df = pd.read_csv(path)
                if 'date' not in str(df.columns[0]).lower(): df = pd.read_csv(path, header=None)
            except:
                df = pd.read_csv(path, header=None)

            if len(df.columns) == 2:
                df.columns = ['date', col_name]

            df['date'] = pd.to_datetime(df['date'])
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
            df.set_index('date', inplace=True)
            df = df.resample('D').mean()
            dfs.append(df)
        except Exception:
            pass  # Si falla uno, seguimos

    if not dfs: return None
    df_base = dfs[0]
    for df in dfs[1:]: df_base = df_base.join(df, how='outer')
    return df_base


# --- 2. CARGA MANUALES ---
def load_manual_data():
    print("--- 2. Cargando datos manuales ---")

    # Eficiencia
    df_eff = None
    try:
        df_eff = pd.read_csv(os.path.join(CARPETA_DATOS, FILE_EFFICIENCY))
        df_eff.columns = ['date', 'efficiency_j_th']
        df_eff['date'] = pd.to_datetime(df_eff['date'])
        df_eff.set_index('date', inplace=True)
        df_eff = df_eff.resample('D').mean().interpolate(method='time')
        print("  ✅ Eficiencia cargada.")
    except:
        print("  ⚠️ Fallo Eficiencia (usando default)")

    # Electricidad (Usando el archivo limpio)
    df_elec = None
    try:
        path_clean = os.path.join(CARPETA_DATOS, FILE_EIA_CLEAN)
        if os.path.exists(path_clean):
            df_elec = pd.read_csv(path_clean)
            df_elec['date'] = pd.to_datetime(df_elec['date'])
            df_elec.set_index('date', inplace=True)
            df_elec = df_elec.resample('D').ffill()  # Rellenar días intermedios
            print("  ✅ Electricidad (Limpia) cargada.")
        else:
            print("  ❌ FALTA 'eia_limpio.csv'. Ejecuta primero limpiar_eia.py")
    except Exception as e:
        print(f"  ❌ Error Electricidad: {e}")

    return df_eff, df_elec


# --- 3. PROCESO FINAL ---
if __name__ == "__main__":
    # A. Blockchain
    df = load_blockchain_files()
    if df is None: exit()

    # B. Manuales
    df_eff, df_elec = load_manual_data()
    if df_eff is not None: df = df.join(df_eff, how='left')
    if df_elec is not None: df = df.join(df_elec, how='left')

    # C. Relleno y Cálculos
    df = df.ffill().bfill()

    # Defaults de seguridad si algo falló
    if 'efficiency_j_th' not in df: df['efficiency_j_th'] = 30.0
    if 'elec_cost_kwh' not in df: df['elec_cost_kwh'] = 0.07

    # Variables Derivadas
    if 'hashrate' in df.columns:
        # Coste Ataque ($/h) = (Hashrate TH/s * J/TH / 1000) * $/kWh
        df['attack_hourly_cost_usd'] = (df['hashrate'] * df['efficiency_j_th'] / 1000) * df['elec_cost_kwh']

    # Filtrar fecha
    df = df[df.index >= pd.to_datetime(FECHA_INICIO)]

    df.to_csv(OUTPUT_FILE)
    print(f"\n🎉 DATASET FINAL GENERADO: {OUTPUT_FILE}")