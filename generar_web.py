import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# --- 1. CARGA Y PREPARACIÓN DE DATOS ---
print("Cargando datos...")
try:
    df = pd.read_csv('dataset_final_btc_ampliado.csv', parse_dates=['date'], index_col='date')
except FileNotFoundError:
    print("❌ Error: No se encuentra 'dataset_final_btc_ampliado.csv'. Ejecuta procesar_datos.py primero.")
    exit()

# Cálculos de KPI para el ataque
# Coste Ataque ($/h) = (Hashrate TH/s * Eficiencia J/TH / 1000 W/kW) * Coste Elec $/kWh
df['attack_hourly_cost_usd'] = (df['hashrate'] * df['efficiency_j_th'] / 1000) * df['elec_cost_kwh']
# Suavizado para visualización limpia
df['attack_cost_sma7'] = df['attack_hourly_cost_usd'].rolling(window=7).mean()

# --- 2. GENERACIÓN DE GRÁFICOS (PLOTLY) ---

# GRÁFICO 1: Contexto (Precio vs Hashrate)
fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(
    go.Scatter(x=df.index, y=df['precio_btc'], name="Precio Bitcoin ($)", line=dict(color='#f7931a')),
    secondary_y=False
)
fig1.add_trace(
    go.Scatter(x=df.index, y=df['hashrate'], name="Hashrate (Seguridad)", line=dict(color='#7f7f7f')),
    secondary_y=True
)
fig1.update_layout(
    title_text="Correlación: Incentivo (Precio) vs Seguridad (Hashrate)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(orientation="h", y=1.1)
)
fig1.update_yaxes(title_text="Precio USD (Log)", type="log", secondary_y=False)
fig1.update_yaxes(title_text="Hashrate TH/s (Log)", type="log", secondary_y=True)
html_fig1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

# GRÁFICO 2: Eficiencia (Eficiencia vs Coste Elec)
fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(
    go.Scatter(x=df.index, y=df['efficiency_j_th'], name="Eficiencia Hardware (J/TH)",
               fill='tozeroy', line=dict(color='#00CC96')),
    secondary_y=False
)
fig2.add_trace(
    go.Scatter(x=df.index, y=df['elec_cost_kwh'], name="Coste Elec. Industrial (USA)",
               line=dict(color='red', dash='dot')),
    secondary_y=True
)
fig2.update_layout(
    title_text="Barreras de Entrada: Evolución Tecnológica y Energética",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(orientation="h", y=1.1)
)
fig2.update_yaxes(title_text="Eficiencia J/TH (Menos es mejor)", secondary_y=False)
fig2.update_yaxes(title_text="Coste $/kWh", secondary_y=True)
html_fig2 = fig2.to_html(full_html=False, include_plotlyjs=False)

# GRÁFICO 3: Coste del Ataque
fig3 = px.area(df, x=df.index, y='attack_hourly_cost_usd',
               title="El Muro de Fuego: Coste Eléctrico por Hora para Atacar Bitcoin (51%)",
               color_discrete_sequence=['#EF553B'])
fig3.update_layout(template="plotly_white", hovermode="x unified")
html_fig3 = fig3.to_html(full_html=False, include_plotlyjs=False)

# --- 3. PLANTILLA HTML CON PESTAÑAS (BOOTSTRAP) ---
# Aquí inyectamos los gráficos generados en una estructura web limpia
html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Análisis de Seguridad Bitcoin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; padding-top: 20px; }}
        .card {{ margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header-title {{ color: #0d6efd; }}
        .nav-tabs .nav-link.active {{ font-weight: bold; border-top: 3px solid #0d6efd; }}
    </style>
</head>
<body>

<div class="container">
    <div class="text-center mb-4">
        <h1 class="header-title">🛡️ Seguridad y Coste de Bitcoin</h1>
        <p class="lead">Análisis visual de la evolución del coste de un ataque del 51%</p>
        <p class="text-muted">Asignatura: Visualización de Datos (M2.859)</p>
    </div>

    <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="tab1-tab" data-bs-toggle="tab" data-bs-target="#tab1" type="button" role="tab">1. Contexto de Red</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab2-tab" data-bs-toggle="tab" data-bs-target="#tab2" type="button" role="tab">2. Barreras de Entrada</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab3-tab" data-bs-toggle="tab" data-bs-target="#tab3" type="button" role="tab">3. Coste del Ataque</button>
        </li>
    </ul>

    <div class="tab-content bg-white p-4 border border-top-0 rounded-bottom" id="myTabContent">

        <div class="tab-pane fade show active" id="tab1" role="tabpanel">
            <h4>La Dimensión de la Red</h4>
            <p>Para entender la seguridad, primero debemos entender el incentivo. El precio impulsa la competencia, lo que eleva el hashrate (potencia de cálculo).</p>
            <div class="card">
                <div class="card-body">
                    {html_fig1}
                </div>
            </div>
        </div>

        <div class="tab-pane fade" id="tab2" role="tabpanel">
            <h4>Eficiencia y Energía</h4>
            <p>La seguridad no depende solo de la cantidad de máquinas, sino de su eficiencia. Los mineros modernos consumen muchos menos Julios por cada Terahash calculado.</p>
            <div class="card">
                <div class="card-body">
                    {html_fig2}
                </div>
            </div>
        </div>

        <div class="tab-pane fade" id="tab3" role="tabpanel">
            <h4>El Coste Real del Ataque</h4>
            <p>Combinando Hashrate, Eficiencia y Coste Eléctrico, obtenemos el coste por hora meramente energético para mantener un ataque del 51%.</p>
            <div class="card">
                <div class="card-body">
                    {html_fig3}
                </div>
            </div>
            <div class="alert alert-warning">
                <strong>Nota:</strong> Este gráfico solo representa el OPEX (Electricidad). No incluye el CAPEX (comprar millones de máquinas), lo cual hace el ataque prácticamente imposible hoy en día.
            </div>
        </div>
    </div>

    <footer class="mt-5 text-center text-muted">
        <small>Datos extraídos de Blockchain.com API & U.S. EIA | Generado con Python & Plotly</small>
    </footer>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# --- 4. GUARDAR ARCHIVO FINAL ---
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("✅ Archivo 'index.html' generado correctamente.")
print("   -> Ahora haz 'git push' y activa GitHub Pages en tu repositorio.")