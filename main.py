import sys
import os
import time

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importar módulos
try:
    import descargar_blockchain
    import limpiar_eia
    import procesar_datos
    import generar_web
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)

def ejecutar_pipeline():
    print("===================================================")
    print("INICIANDO PIPELINE DE DATOS BITCOIN SECURITY")
    print("===================================================")

    # PASO 1: Descarga
    print("\n[1/4] EJECUTANDO: Descarga de datos...")
    descargar_blockchain.main()

    # PASO 2: Limpieza EIA
    print("\n[2/4] EJECUTANDO: Limpieza de datos EIA...")
    limpiar_eia.main()

    # PASO 3: Procesado
    print("\n[3/4] EJECUTANDO: Procesamiento y Fusión...")
    procesar_datos.main()

    # PASO 4: Web
    print("\n[4/4] EJECUTANDO: Generación de Web...")
    # Asegúrate de que generar_web.py también tenga un def main() o usa generar_pagina() si así lo llamaste
    if hasattr(generar_web, 'main'):
        generar_web.main()
    elif hasattr(generar_web, 'generar_pagina'):
        generar_web.generar_pagina()
    else:
        # Si generar_web está suelto, lo ejecutamos recargando el módulo o asumiendo que ya corrió al importar
        print("Advertencia: generar_web no tiene función main(), verifica su ejecución.")

    print("\nTODO LISTO. Abre 'index.html' para ver el resultado.")

if __name__ == "__main__":
    ejecutar_pipeline()