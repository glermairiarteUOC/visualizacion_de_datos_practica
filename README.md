# 📈 Visualización: Seguridad y Coste de Bitcoin

Este proyecto analiza la evolución del coste de un ataque del 51% a la red Bitcoin, cruzando métricas on-chain con la eficiencia del hardware de minería y los costes energéticos.

**Proyecto para la asignatura M2.859 - Visualización de Datos.**

---

### Estado Actual

Proyecto en **Fase 2: Configuración del Repositorio**.

**Próximos Pasos:**
1.  [X] **Paso 1:** Adquisición de datos (Fuentes localizadas).
2.  [X] **Paso 2:** Configuración de repositorio y documentación.
3.  [ ] **Paso 3:** Cargar y limpiar los 7 archivos de datos (BTC, EIA, Eficiencia).
4.  [ ] **Paso 4:** Unificar los dataframes en una única tabla diaria.
5.  [ ] **Paso 5:** Calcular las métricas derivadas (coste de ataque, etc.).

---

### 🚀 Cómo Empezar

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/visualizacion-btc-seguridad.git](https://github.com/TU_USUARIO/visualizacion-btc-seguridad.git)
    cd visualizacion-btc-seguridad
    ```

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # (En Mac/Linux)
    .venv\Scripts\activate     # (En Windows)
    ```

3.  **Instalar dependencias:**
    *(Crearemos un `requirements.txt` más tarde)*
    ```bash
    pip install requests pandas openpyxl
    ```
    *(Nota: `openpyxl` será necesario para leer el archivo `.xls` de la EIA)*

4.  **Obtener los datos:**
    Sigue las instrucciones de la sección **"Adquisición de Datos"** más abajo para poblar tu carpeta local `datos_csv/`.

---

### 🛠️ Adquisición de Datos

Para que el proyecto funcione, los datos brutos deben descargarse y colocarse en la carpeta `datos_csv/` (la cual está ignorada por Git).

#### Fuente 1: Datos de Bitcoin (Blockchain.com)

Estos datos se obtienen automáticamente ejecutando nuestro script de Python.

1.  Asegúrate de tener `requests` instalado (`pip install requests`).
2.  Ejecuta el script:
    ```bash
    python descargar_blockchain.py
    ```
3.  Esto creará los 5 archivos CSV de Bitcoin dentro de `datos_csv/`.

#### Fuente 2: Coste Eléctrico (EIA)

Estos datos deben descargarse manualmente.

1.  Visita el "Data Browser" de la EIA: [https://www.eia.gov/electricity/data/browser/](https://www.eia.gov/electricity/data/browser/)
2.  **Categoría:** En la columna izquierda, haz clic en **"Retail Sales and Price"**.
3.  **Frecuencia:** Haz clic en **"Monthly"**.
4.  **Selección:**
    * En "Data Series", marca **"Average price"**.
    * En "Geography", verifica que sea **"U.S. Total"**.
    * En "Sector", desmarca "Total (All Sectors)" y marca únicamente **"Industrial"**.
5.  Haz clic en el botón azul **"Get Data"**.
6.  En la nueva página, busca la pestaña o botón **"Download"** o **"Export"** y descarga el archivo (usualmente `.xls` o `.csv`).
7.  **Guarda** este archivo en la carpeta `datos_csv/` con el nombre `precio_electricidad_eia.xls` (o `.csv` si es el caso).

#### Fuente 3: Eficiencia de Minería (Manual - CCAF)

Esta es una serie temporal manual basada en los datos de eficiencia de hardware (ASICs) publicados por el Cambridge Centre for Alternative Finance (CCAF) y otros análisis de la industria.

1.  Abre el archivo `datos_csv/efficiency_manual.csv` que creaste.
2.  **Pega el siguiente contenido** en él (reemplazando la cabecera que ya tenías):

```csv
date,efficiency_j_th
2009-01-03,10000000
2010-12-01,600000
2011-06-01,50000
2013-02-01,10000
2013-12-01,2000
2015-05-01,500
2016-06-01,150
2018-03-01,100
2019-05-01,60
2020-05-01,45
2021-05-01,35
2022-12-01,30
2024-01-01,20