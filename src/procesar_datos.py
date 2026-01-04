import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
# Rutas relativas desde la raíz
FOLDER_API = "datos/raw_api"
FILE_EFFICIENCY = "datos/raw_manual/efficiency_manual.csv"
FILE_EIA_CLEAN = "datos/processed/eia_limpio.csv"

# CAMBIO: Nombre final ajustado
OUTPUT_FILE = "datos/processed/dataset_final_btc.csv"


def load_blockchain_files():
    print("--- 1. Cargando datos de Blockchain.com ---")
    if not os.path.exists(FOLDER_API):
        print(f"La carpeta '{FOLDER_API}' no existe.")
        return None

    dfs = []
    csv_files = [f for f in os.listdir(FOLDER_API) if f.endswith('.csv')]

    if not csv_files:
        print(f"No hay CSVs en {FOLDER_API}.")
        return None

    for file_name in csv_files:
        path = os.path.join(FOLDER_API, file_name)
        col_name = file_name.replace('.csv', '')
        try:
            df = pd.read_csv(path, names=['date', col_name], header=None)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df = df.resample('D').mean()
            dfs.append(df)
        except Exception as e:
            print(f"Error leyendo {file_name}: {e}")

    if not dfs: return None

    print(f"  -> Fusionando {len(dfs)} archivos de API...")
    return pd.concat(dfs, axis=1)


def load_manual_data():
    print("--- 2. Cargando datos manuales ---")
    df_eff = None
    df_elec = None

    # Eficiencia
    if os.path.exists(FILE_EFFICIENCY):
        try:
            df_eff = pd.read_csv(FILE_EFFICIENCY)
            df_eff['date'] = pd.to_datetime(df_eff['date'])
            df_eff.set_index('date', inplace=True)
            df_eff = df_eff.resample('D').interpolate(method='linear')
            print("Eficiencia cargada.")
        except Exception as e:
            print(f"Error Eficiencia: {e}")
    else:
        print(f"No existe {FILE_EFFICIENCY} (usando defaults).")

    # Electricidad
    if os.path.exists(FILE_EIA_CLEAN):
        try:
            df_elec = pd.read_csv(FILE_EIA_CLEAN)
            df_elec['date'] = pd.to_datetime(df_elec['date'])
            df_elec.set_index('date', inplace=True)
            df_elec = df_elec.resample('D').ffill()
            print("Electricidad cargada.")
        except Exception as e:
            print(f"Error Electricidad: {e}")
    else:
        print(f"FALTA '{FILE_EIA_CLEAN}'. Ejecuta limpiar_eia.py primero.")

    return df_eff, df_elec


# --- FUNCIÓN PRINCIPAL ---
def main():
    print("--- 3. Procesando y fusionando datos ---")

    # 1. API
    df = load_blockchain_files()
    if df is None:
        print("Saltando proceso por falta de datos API.")
        return

    # 2. Manuales
    df_eff, df_elec = load_manual_data()

    # 3. Join
    if df_eff is not None: df = df.join(df_eff, how='left')
    if df_elec is not None: df = df.join(df_elec, how='left')

    # 4. Limpieza
    df = df.ffill().bfill()

    if 'efficiency_j_th' not in df: df['efficiency_j_th'] = 15.0
    if 'elec_cost_kwh' not in df: df['elec_cost_kwh'] = 0.05

    # 5. Guardar
    df.to_csv(OUTPUT_FILE)
    print(f"Dataset maestro guardado en: {OUTPUT_FILE}")
    print("procesar_datos.py finalizado.")


if __name__ == "__main__":
    main()