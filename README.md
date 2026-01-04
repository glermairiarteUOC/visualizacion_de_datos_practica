# 📈 Visualización: Bitcoin Security Analysis

Este proyecto analiza la evolución del coste de un ataque del 51% a la red Bitcoin, cruzando métricas *on-chain* con la eficiencia del hardware de minería y los costes energéticos industriales.

**Proyecto para la asignatura M2.859 - Visualización de Datos (UOC).**

---

## 📂 Estructura del Repositorio

El proyecto está modularizado para separar la descarga, limpieza, procesamiento y visualización de los datos.

```text
.
├── main.py                     # Script principal (Orquestador del pipeline)
├── src/                        # Módulos de procesamiento
│   ├── descargar_blockchain.py # Descarga datos de la API de Blockchain.com
│   ├── limpiar_eia.py          # Procesa datos de electricidad (EIA)
│   ├── procesar_datos.py       # Fusiona datasets y calcula métricas
│   └── generar_web.py          # Genera el dashboard HTML con Plotly
├── datos/                      # Almacenamiento de datos
│   ├── raw_api/                # Datos crudos descargados automáticamente
│   ├── raw_manual/             # Datos ingresados manualmente (Electricidad/Eficiencia)
│   └── processed/              # Dataset final limpio (dataset_final_btc.csv)
├── index.html                  # Resultado final: Dashboard interactivo
└── README.md                   # Documentación del proyecto
```

## 🚀 Guía de Uso

Sigue estos pasos para descargar el repositorio, configurar el entorno y generar el dashboard en tu máquina local.
1. Prerrequisitos

Necesitas tener instalado Python 3.8+. Además, este proyecto requiere las siguientes librerías:

    pandas
    plotly
    requests

2. Instalación

Abre tu terminal y ejecuta los siguientes comandos:
Bash

#### A. Clonar el repositorio (sustituye tu-usuario y nombre-repo por los reales)
    git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)

#### B. Entrar en la carpeta del proyecto
    cd nombre-del-repo

#### C. Instalar las dependencias necesarias
    pip install pandas plotly requests

3. Configuración de Datos Manuales

Debido a que algunas fuentes no ofrecen API pública gratuita, es necesario asegurarse de que los archivos manuales existan en la carpeta datos/raw_manual/:

    Precio de la Electricidad: El script espera Average_retail_price_of_electricity_monthly.csv (formato EIA).
    Eficiencia Minera: El script espera efficiency_manual.csv (con columnas date y efficiency_j_th).

4. Ejecución

Una vez configurado, ejecuta el script principal que orquesta todo el proceso (descarga, limpieza, procesamiento y generación web):
Bash

    python main.py

Verás en la consola el progreso del pipeline paso a paso:

    Descarga de datos de Blockchain.com.
    Limpieza de datos de la EIA.
    Procesamiento y fusión de CSVs.
    Generación del archivo index.html.

5. Visualización

Al finalizar, se creará (o actualizará) el archivo index.html en la raíz del proyecto. Simplemente abre este archivo con tu navegador web favorito (Chrome, Firefox, Edge) para interactuar con la visualización.

## 🛠️ Tecnologías Utilizadas

    Python: Lenguaje principal.

    Pandas: Manipulación y análisis de datos (ETL).

    Plotly: Librería de gráficos interactivos.

    Bootstrap 5: Estilizado del dashboard HTML final.

    APIs: Blockchain.com (datos de red).

## 🗄️ Obtención de datos

#### 1. Blockchain.com (Automático)

Ampliación significativa para capturar el estado de la red en tres dimensiones:

    Mercado: Precio, Market Cap, Volumen Exchange.

    Minería: Hashrate, Dificultad, Ingresos (Revenue).

    Red: Transacciones/seg, Tamaño Mempool, Fees, Direcciones Únicas, Tamaño Bloque, Total BTC en circulación.

#### 2. Datos de Electricidad (Manual)
Utilizamos el precio medio de la electricidad industrial en EE.UU. como proxy del coste energético global de los mineros.

* **Fuente:** U.S. Energy Information Administration (EIA).
* **URL:** [Electric Power Monthly - Average Retail Price of Electricity](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a)
* **Pasos:**
    1.  Ir a la tabla "Average Retail Price of Electricity to Ultimate Customers".
    2.  Buscar la sección **"Industrial"**.
    3.  Descargar el histórico completo (seleccionar opción "Download" o copiar la tabla).
    4.  Guardar el archivo como: `datos/raw_manual/Average_retail_price_of_electricity_monthly.csv`.
    5.  *Formato esperado:* CSV delimitado por punto y coma (`;`) o coma, con columnas `Month` (ej: Apr 2024) y `Price` (Cents/kWh).

#### 3. Datos de Eficiencia Minera (Manual)
La eficiencia mide cuánta energía (Julios) se necesita para calcular un Terahash. Como no existe un registro centralizado, construimos una curva basada en los lanzamientos de hardware más populares (ej. Antminer S9, S19, S21).

* **Fuente:** [ASIC Miner Value](https://www.asicminervalue.com/) o Notas de prensa de fabricantes (Bitmain, MicroBT).
* **Archivo:** `datos/raw_manual/efficiency_manual.csv`.
* **Formato:** Debes mantener actualizado este archivo CSV con dos columnas:
    ```csv
    date,efficiency_j_th
    2015-01-01,250.0
    2016-06-01,100.0
    2020-05-01,30.0
    2024-01-01,17.5
    ```
* **Lógica:** El sistema interpolará linealmente los valores entre estas fechas para estimar la eficiencia media de la red día a día. Si sale un nuevo minero revolucionario, añade una nueva fila con la fecha de lanzamiento y su eficiencia.