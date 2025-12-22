# 📈 Visualización: Seguridad y Coste de Bitcoin

Este proyecto analiza la evolución del coste de un ataque del 51% a la red Bitcoin, cruzando métricas on-chain con la eficiencia del hardware de minería y los costes energéticos industriales.

**Proyecto para la asignatura M2.859 - Visualización de Datos.**

---

## 🚦 Estado Actual

**Fase 4 (Iteración 2): Enriquecimiento del Dataset.**
Siguiendo el feedback recibido, se ha ampliado la recolección de datos para superar las **20 variables analíticas**, incluyendo métricas de estado de la red (Mempool, Fees) y **atributos derivados** (Medias móviles, Volatilidad, Ratios financieros) para facilitar el diseño de la visualización final.

**Progreso:**
- [x] **Paso 1:** Adquisición masiva de datos (15+ métricas base de Blockchain.com).
- [x] **Paso 2:** Configuración de repositorio y entorno virtual.
- [x] **Paso 3:** Limpieza (ETL) y normalización con **resampleo diario** para sincronización perfecta.
- [x] **Paso 4:** Feature Engineering (Cálculo de SMA, Volatilidad, NVT Ratio, Hashprice).
- [x] **Paso 5:** Definición de Roles Analíticos (Hechos vs Dimensiones).
- [ ] **Paso 6:** Análisis y Visualización final (Tableau/Python).

---

## 📂 Estructura del Repositorio

```text
visualizacion-btc-seguridad/
│
├── .venv/                          # Entorno virtual (no se sube a Git)
│
├── datos_csv/                      # Carpeta de DATOS BRUTOS
│   ├── precio_btc.csv              # [Base] Precio mercado (USD)
│   ├── hashrate.csv                # [Base] Hashrate total
│   ├── mempool_size.csv            # [Base] Congestión de red (Nuevo)
│   ├── fees_total_btc.csv          # [Base] Comisiones pagadas (Nuevo)
│   ├── ... (10+ archivos más)      # Resto de métricas crudas
│   ├── efficiency_manual.csv       # [Manual] Histórico eficiencia hardware (J/TH)
│   └── Average_retail_price...csv  # [Manual] Precio electricidad industrial (EIA)
│
├── descargar_blockchain.py         # Script 1: Descarga automática de 15 APIs
├── procesar_datos.py               # Script 2: ETL, Resampleo Diario y Feature Engineering
├── dataset_final_btc_ampliado.csv  # RESULTADO: Dataset maestro (>20 vars) listo para analizar
│
├── .gitignore                      # Archivos ignorados
└── README.md                       # Documentación y Diccionario de Datos
```

## 🚀 Guía de Uso Rápida
1. Preparación del Entorno

```text
git clone [https://github.com/TU_USUARIO/visualizacion-btc-seguridad.git](https://github.com/TU_USUARIO/visualizacion-btc-seguridad.git)
cd visualizacion-btc-seguridad

# Crear entorno virtual
python -m venv .venv

# Activar (Windows):
.venv\Scripts\activate
# Activar (Mac/Linux):
# source .venv/bin/activate

# Instalar dependencias
pip install requests pandas matplotlib seaborn openpyxl
```

2. Ejecución del Pipeline ETL


A. Descarga de datos frescos:

```text
python descargar_blockchain.py
```

Este script descarga automáticamente 15 datasets históricos diferentes desde la API de Blockchain.info.

B. Procesamiento y Generación de Variables:

```text
python procesar_datos.py
```

Realiza las siguientes tareas críticas:

    Carga todos los CSVs y normaliza nombres.

    Resampleo Diario (.resample('D')): Alinea todas las métricas a las 00:00:00, promediando valores si existen duplicados, solucionando desajustes horarios entre fuentes.

    Feature Engineering: Calcula variables derivadas (SMA, Volatilidad, Ratios).

    Unión: Cruza con datos manuales (Electricidad y Eficiencia).

    Exportación: Genera el archivo dataset_final_btc_ampliado.csv.

## 📊 Diccionario de Datos y Roles Analíticos

Para facilitar el diseño de la visualización, se han definido los roles de cada variable según el modelo dimensional. Se han incluido métricas derivadas para cumplir con el requisito de "decenas de variables".
Variable,Descripción,Rol Analítico,Origen
ariable	Descripción	Rol Analítico	Origen
Date	Fecha del registro (Diario, normalizado)	Dimensión (Tiempo)	Index
price_usd	Precio de cierre de Bitcoin (USD)	Hecho	API
market_cap_usd	Capitalización de mercado total	Hecho	API
hashrate	Potencia de cálculo de la red (TH/s)	Hecho	API
difficulty	Dificultad de minado (ajuste automático)	Hecho	API
miners_rev_usd	Ingresos totales mineros (Bloque + Fees) en USD	Hecho	API
mempool_size	Tamaño de la mempool (Bytes) - Congestión	Hecho	API
unique_addr	Número de direcciones únicas activas	Hecho	API
tx_count	Número de transacciones diarias	Hecho	API
fees_btc	Total comisiones pagadas a mineros (BTC)	Hecho	API
avg_block_size	Tamaño promedio del bloque (MB)	Hecho	API
efficiency_j_th	Eficiencia del hardware minero (J/TH)	Hecho	Manual
elec_cost_kwh	Coste electricidad industrial (USD/kWh)	Hecho	Manual (EIA)
price_sma7	Media móvil precio (7 días) - Tendencia CP	Hecho Derivado	Calculado
price_sma30	Media móvil precio (30 días) - Tendencia MP	Hecho Derivado	Calculado
price_volatility	Volatilidad (Desv. Estándar 30 días)	Hecho Derivado	Calculado
price_pct_change	Variación porcentual diaria del precio	Hecho Derivado	Calculado
nvt_ratio	Ratio Valor Red / Transacciones (Métrica de valoración)	Hecho Derivado	Calculado
hashprice_usd	Ingresos estimados por unidad de Hashrate	Hecho Derivado	Calculado

## 🛠️ Detalle de Fuentes de Datos
1. Blockchain.com (Automático)

Ampliación significativa para capturar el estado de la red en tres dimensiones:

    Mercado: Precio, Market Cap, Volumen Exchange.

    Minería: Hashrate, Dificultad, Ingresos (Revenue).

    Red: Transacciones/seg, Tamaño Mempool, Fees, Direcciones Únicas, Tamaño Bloque, Total BTC en circulación.

2. U.S. EIA (Manual)

    Archivo: Average_retail_price_of_electricity_monthly.csv

    Dato: Coste medio de la electricidad industrial en EE.UU. Se utiliza como proxy del coste energético global ("OPEX") de los mineros.

3. Eficiencia Hardware (Manual)

    Archivo: efficiency_manual.csv

    Metodología: Interpolación lineal entre hitos de lanzamiento de hardware ASICS principales (Bitmain Antminer S9, S19, XP, etc.).

```text
Ejemplo de datos de eficiencia interpolados:
2016-06-01 -> 98.0 J/TH (Era Antminer S9)
2020-05-01 -> 34.5 J/TH (Era Antminer S19)
2024-01-01 -> 15.0 J/TH (Hardware de última generación)
```