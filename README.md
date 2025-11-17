📈 Visualización: Seguridad y Coste de Bitcoin

Este proyecto analiza la evolución del coste de un ataque del 51% a la red Bitcoin, cruzando métricas on-chain con la eficiencia del hardware de minería y los costes energéticos industriales.

Proyecto para la asignatura M2.859 - Visualización de Datos.

🚦 Estado Actual

Fase 4: Análisis y Visualización. Hemos completado la ingeniería de datos (ETL). Los datos brutos han sido limpiados, sincronizados temporalmente y exportados a un dataset maestro listo para el análisis.

Progreso:

    [x] Paso 1: Adquisición de datos (Scripts y fuentes localizadas).

    [x] Paso 2: Configuración de repositorio y entorno.

    [x] Paso 3: Limpieza de datos (ETL) y normalización de fechas.

    [x] Paso 4: Unificación de fuentes (Blockchain + EIA + Eficiencia) en un solo CSV.

    [ ] Paso 5: Script de Análisis (Cálculo de métricas de seguridad y coste).

    [ ] Paso 6: Generación de visualizaciones finales.

📂 Estructura del Repositorio

Plaintext

### 📂 Estructura del Repositorio

```text
visualizacion-btc-seguridad/
│
├── .venv/                          # Entorno virtual de Python (no se sube a Git)
│
├── datos_csv/                      # Carpeta de DATOS BRUTOS (ignorada por Git)
│   ├── precio_btc.csv              # [Auto] Precio de mercado diario (USD)
│   ├── hashrate_btc.csv            # [Auto] Hashrate total de la red
│   ├── dificultad_btc.csv          # [Auto] Dificultad de minado
│   ├── transacciones_btc.csv       # [Auto] Número de transacciones diarias
│   ├── ingresos_mineros_btc.csv    # [Auto] Ingresos totales mineros (USD)
│   ├── efficiency_manual.csv       # [Manual] Histórico eficiencia hardware (J/TH)
│   └── Average_retail_price...csv  # [Manual] Precio electricidad industrial (EIA)
│
├── descargar_blockchain.py         # Script 1: Descarga automática de APIs
├── procesar_datos.py               # Script 2: Limpieza (ETL), normalización y cálculo BTC
├── analisis_seguridad.py           # Script 3: (Fase 4) Análisis de costes y Gráficos
│
├── dataset_completo_bitcoin.csv    # RESULTADO: Dataset maestro limpio (Input para Script 3)
├── .gitignore                      # Archivos ignorados (venv, __pycache__, datos_csv)
└── README.md                       # Documentación del proyecto
```

### 🚀 Guía de Uso Rápida

1.  **Clonar el repositorio y preparar entorno:**
    ```bash
    git clone [https://github.com/TU_USUARIO/visualizacion-btc-seguridad.git](https://github.com/TU_USUARIO/visualizacion-btc-seguridad.git)
    cd visualizacion-btc-seguridad
    
    # Crear entorno virtual
    python -m venv .venv
    
    # Activar entorno (Windows):
    .venv\Scripts\activate
    
    # Activar entorno (Mac/Linux):
    # source .venv/bin/activate
    
    # Instalar librerías necesarias
    pip install requests pandas matplotlib seaborn openpyxl
    ```

2.  **Paso 1: Descargar Datos Automáticos:**
    ```bash
    python descargar_blockchain.py
    ```
    *(Esto descargará los datos de precio, hashrate, etc. en la carpeta `datos_csv/`)*

3.  **Paso 2: Asegurar Datos Manuales:**
    * Verifica que el archivo `efficiency_manual.csv` y el archivo de la EIA (`Average_retail_price...`) se encuentren dentro de la carpeta `datos_csv/`.

4.  **Paso 3: Procesar y Limpiar (ETL):**
    ```bash
    python procesar_datos.py
    ```
    * Este script normaliza las fechas, rellena huecos, calcula los ingresos en BTC y genera el archivo maestro **`dataset_completo_bitcoin.csv`**.

### 🛠️ Fuentes de Datos (Detalle)

1. Datos de Bitcoin (Automático)

Fuente: Blockchain.com API. Se obtienen mediante descargar_blockchain.py. Incluye: Precio, Hashrate, Dificultad, Transacciones e Ingresos Mineros.

2. Coste Eléctrico (Manual)

Fuente: U.S. Energy Information Administration (EIA).

    Archivo requerido en datos_csv/: Average_retail_price_of_electricity_monthly.csv

    Filtros usados: Sector Industrial, Frecuencia Mensual.

3. Eficiencia de Minería (Manual)

Fuente: Recopilación basada en hitos de hardware (Bitmain Antminer S9, S19, etc.) y datos del CCAF.
Archivo: datos_csv/efficiency_manual.csv.

Contenido actual del archivo de eficiencia (J/TH):

```text
date,efficiency_j_th
2009-01-03,800000.0
2010-10-01,290000.0
2011-06-01,45000.0
2013-01-01,10000.0
2013-11-01,2000.0
2014-07-01,770.0
2014-12-01,510.0
2015-08-01,250.0
2016-06-01,98.0
2018-12-01,57.0
2019-04-01,40.0
2020-05-01,34.5
2020-05-02,29.5
2021-11-01,21.5
2023-09-01,17.5
2024-01-01,15.0
```