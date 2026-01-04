import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- CONFIGURACIÓN DE RUTAS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_FILE = os.path.join(BASE_DIR, "datos", "processed", "dataset_final_btc.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")


def main():
    print("Generando dashboard...")

    if not os.path.exists(INPUT_FILE):
        print(f"Error: No se encuentra '{INPUT_FILE}'.")
        return

    # 1. CARGA DE DATOS
    df = pd.read_csv(INPUT_FILE, parse_dates=['date'], index_col='date')
    df.sort_index(inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    # 2. CÁLCULOS DERIVADOS
    df['network_power_gw'] = (df['hashrate'] * df['efficiency_j_th']) / 1e9
    df['attack_hourly_cost_usd'] = (df['hashrate'] * df['efficiency_j_th'] / 1000) * df['elec_cost_kwh']

    # --- GENERACIÓN DE GRÁFICOS ---

    # ---------------------------------------------------------
    # PESTAÑA 2: MERCADO Y ADOPCIÓN (4 Variables)
    # ---------------------------------------------------------
    fig_market = make_subplots(
        rows=2, cols=2,
        shared_xaxes=True, vertical_spacing=0.1, horizontal_spacing=0.08,
        subplot_titles=("Precio de mercado", "Volumen de exchange", "Direcciones usadas diarias",
                        "Transacciones diarias")
    )
    # 1. Precio
    fig_market.add_trace(
        go.Scatter(x=df.index, y=df['precio_btc'], name="Precio de mercado (USD)", line=dict(color='#F7931A')),
        row=1, col=1)
    # 2. Volumen
    fig_market.add_trace(
        go.Scatter(x=df.index, y=df['trade_volume_exchange'], name="Volumen de exchange (USD)",
                   line=dict(color='#6c757d')), row=1, col=2)
    # 3. Direcciones
    fig_market.add_trace(
        go.Scatter(x=df.index, y=df['n_unique_addresses'], name="Direcciones usadas diarias",
                   line=dict(color='#007bff')), row=2,
        col=1)
    # 4. Transacciones
    fig_market.add_trace(
        go.Scatter(x=df.index, y=df['transacciones_dia'], name="Transacciones diarias", line=dict(color='#28a745'),
                   opacity=0.5), row=2, col=2)

    # Ejes Y (Verticales): Personalizados según la métrica
    fig_market.update_yaxes(title_text="USD", row=1, col=1)
    fig_market.update_yaxes(title_text="USD", row=1, col=2)
    fig_market.update_yaxes(title_text="Nº Direcciones", row=2, col=1)
    fig_market.update_yaxes(title_text="Nº Transacciones", row=2, col=2)

    # Ejes X (Horizontales): Como es compartido (shared_xaxes=True), basta con ponerlo en la fila inferior
    fig_market.update_xaxes(title_text="Fecha", row=2, col=1)
    fig_market.update_xaxes(title_text="Fecha", row=2, col=2)

    # Height: 600px | Margin top (t): 30px
    fig_market.update_layout(height=600, template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), showlegend=False)

    # ---------------------------------------------------------
    # PESTAÑA 3: INFRAESTRUCTURA (4 Variables)
    # ---------------------------------------------------------
    fig_infra = make_subplots(
        rows=2, cols=2,
        shared_xaxes=True, vertical_spacing=0.1, horizontal_spacing=0.08,
        subplot_titles=("Hashrate", "Dificultad de bloque", "Tamaño de la mempool", "Tamaño promedio de bloque")
    )
    # 1. Hashrate
    fig_infra.add_trace(go.Scatter(x=df.index, y=df['hashrate'], name="Hashrate", line=dict(color='#4D4D4D')), row=1,
                        col=1)
    fig_infra.update_yaxes(type="log", row=1, col=1)
    # 2. Dificultad
    fig_infra.add_trace(
        go.Scatter(x=df.index, y=df['dificultad'], name="Dificultad de bloque", line=dict(color='#dc3545', dash='dot')),
        row=1,
        col=2)
    # 3. Mempool
    fig_infra.add_trace(
        go.Scatter(x=df.index, y=df['mempool_size'], name="Tamaño de la mempool", line=dict(color='#6f42c1')), row=2,
        col=1)
    # 4. Tamaño Bloque
    fig_infra.add_trace(
        go.Scatter(x=df.index, y=df['avg_block_size'], name="Tamaño promedio de bloque", line=dict(color='#17a2b8')),
        row=2, col=2)

    # Ejes Y (Verticales): Personalizados según la métrica
    fig_infra.update_yaxes(title_text="TH/s", row=1, col=1)
    fig_infra.update_yaxes(title_text="Dificultad", row=1, col=2)
    fig_infra.update_yaxes(title_text="Bytes", row=2, col=1)
    fig_infra.update_yaxes(title_text="MB", row=2, col=2)

    # Ejes X (Horizontales): Como es compartido (shared_xaxes=True), basta con ponerlo en la fila inferior
    fig_infra.update_xaxes(title_text="Fecha", row=2, col=1)
    fig_infra.update_xaxes(title_text="Fecha", row=2, col=2)

    fig_infra.update_layout(height=600, template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), showlegend=False,
                            autosize=True, width=None)

    # ---------------------------------------------------------
    # PESTAÑA 4: ECONOMÍA DE LA SEGURIDAD (4 Variables)
    # ---------------------------------------------------------
    fig_security = make_subplots(
        rows=2, cols=2, shared_xaxes=True, vertical_spacing=0.1, horizontal_spacing=0.08,
        subplot_titles=("Coste de un ataque del 51%", "Ingresos de los mineros", "Total fees recaudados",
                        "Coste por transacción")
    )
    # 1. Coste Ataque
    fig_security.add_trace(
        go.Scatter(x=df.index, y=df['attack_hourly_cost_usd'], name="Coste de un ataque del 51%",
                   line=dict(color='red')), row=1,
        col=1)
    fig_security.update_yaxes(type="log", row=1, col=1)
    # 2. Ingresos Mineros
    fig_security.add_trace(
        go.Scatter(x=df.index, y=df['miners_revenue_usd'], name="Ingresos de los mineros", fill='tozeroy',
                   line=dict(color='#28a745')),
        row=1, col=2)
    # 3. Fees Totales
    fig_security.add_trace(
        go.Scatter(x=df.index, y=df['fees_total_btc'], name="Total fees recaudados",
                   line=dict(color='orange', dash='dash')),
        row=2, col=1)
    # 4. Coste por Tx
    fig_security.add_trace(
        go.Scatter(x=df.index, y=df['cost_per_tx'], name="Coste por transacción", line=dict(color='#20c997')),
        row=2, col=2)

    # Ejes Y (Verticales): Personalizados según la métrica
    fig_security.update_yaxes(title_text="USD/h", row=1, col=1)
    fig_security.update_yaxes(title_text="USD", row=1, col=2)
    fig_security.update_yaxes(title_text="Bitcoin", row=2, col=1)
    fig_security.update_yaxes(title_text="USD/transaccion", row=2, col=2)

    # Ejes X (Horizontales): Como es compartido (shared_xaxes=True), basta con ponerlo en la fila inferior
    fig_security.update_xaxes(title_text="Fecha", row=2, col=1)
    fig_security.update_xaxes(title_text="Fecha", row=2, col=2)

    # Height: 600px | Margin top (t): 30px
    fig_security.update_layout(height=600, template="plotly_white", margin=dict(l=20, r=20, t=30, b=20),
                               showlegend=False)

    # --- HTML STRING GENERATION ---
    plot_market_html = fig_market.to_html(full_html=False, include_plotlyjs='cdn', default_width='100%',
                                          config={'responsive': True})
    plot_infra_html = fig_infra.to_html(full_html=False, include_plotlyjs='cdn', default_width='100%',
                                        config={'responsive': True})
    plot_security_html = fig_security.to_html(full_html=False, include_plotlyjs='cdn', default_width='100%',
                                              config={'responsive': True})

    # --- TEMPLATE HTML COMPLETO ---
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Bitcoin Security Analysis</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f4f7f6; font-family: 'Segoe UI', sans-serif; }}
            .nav-pills .nav-link.active {{ background-color: #F7931A; }}

            .tab-pane:not(.active) {{ display: none !important; }}

            .card {{ border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: none; margin-bottom: 10px; }}
            .header-bg {{ background: #1e1e1e; color: white; padding: 20px 0; }}
            .kpi-box {{ text-align: center; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}

            .info-text h5 {{ color: #F7931A; font-weight: bold; margin-top: 15px; font-size: 1.1rem; }}
            .info-text p {{ font-size: 0.9rem; color: #666; text-align: justify; line-height: 1.5; }}
            .info-text h3 {{ font-size: 1.5rem; color: #333; }}

            /* ESTILOS PARA LA CONCLUSIÓN */
            .conclusion-box {{
                background-color: #e3f2fd; /* Azul muy suave */
                border-left: 5px solid #2196F3; /* Borde azul fuerte */
            }}
            .conclusion-title {{
                color: #0d47a1;
                font-weight: bold;
                font-size: 1.1rem;
            }}
        </style>
    </head>
    <body>
        <div class="header-bg text-center mb-3">
            <h1 class="display-4 fw-bold">Bitcoin <span style="color:#F7931A">Security</span> Analysis</h1>
            <p class="lead">Visualización avanzada de métricas on-chain y de la infraestructura de bitcoin para analizar la seguridad de la red</p>
        </div>

        <div class="container-fluid px-5">

            <div class="row mb-3">
                <div class="col-md-3"><div class="kpi-box"><h6>Precio BTC</h6><h3 class="fw-bold">${df['precio_btc'].iloc[-1]:,.0f}</h3></div></div>
                <div class="col-md-3"><div class="kpi-box"><h6>Hashrate actual</h6><h3 class="fw-bold">{df['hashrate'].iloc[-1] / 1e6:.1f} EH/s</h3></div></div>
                <div class="col-md-3"><div class="kpi-box"><h6>Potencia de la red</h6><h3 class="fw-bold text-primary">{df['network_power_gw'].iloc[-1]:.2f} GW</h3></div></div>
                <div class="col-md-3"><div class="kpi-box"><h6>Coste por hora de un ataque</h6><h3 class="fw-bold text-danger">${df['attack_hourly_cost_usd'].iloc[-1]:,.0f}/h</h3></div></div>
            </div>

            <ul class="nav nav-pills nav-fill mb-3 p-2 bg-white rounded shadow-sm" id="myTab" role="tablist">
                <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab1" type="button">Proyecto</button></li>
                <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab2" type="button">Precio y uso de la red</button></li>
                <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab3" type="button">Infraestructura de Bitcoin</button></li>
                <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab4" type="button">Seguridad y coste de un ataque</button></li>
            </ul>

            <div class="tab-content">

                <div class="tab-pane fade show active" id="tab1">
                    <div class="card p-4">
                        <h2 class="mb-3 text-primary border-bottom pb-3">Metodología y alcance del proyecto</h2>

                        <div class="row mb-3">
                            <div class="col-12">
                                <p class="lead text-dark">
                                    Este dashboard presenta un análisis de la red Bitcoin, correlacionando su valoración de mercado con la seguridad de la red y la económica subyacente.
                                </p>
                                <p style="text-align: justify;">
                                    El objetivo es visualizar la <strong>escalabilidad de la seguridad</strong>: determinar si el crecimiento en el precio y la adopción está respaldado por una infraestructura física robusta (Hashrate) y un modelo de incentivos económicos sostenible a largo plazo. Para ello, se han procesado y normalizado <strong>12 variables críticas</strong> divididas en tres vectores de análisis.
                                </p>
                            </div>
                        </div>

                        <div class="row text-center mt-3">
                            <div class="col-md-4 mb-3">
                                <div class="p-3 border rounded bg-light h-100">
                                    <h5 style="color:#F7931A;">1. Precio y uso de la red</h5>
                                    <p class="small text-muted mb-2">Evalúa la demanda y el uso real.</p>
                                    <hr>
                                    <ul class="list-unstyled text-start small ps-3">
                                        <li>• Precio de mercado (USD)</li>
                                        <li>• Volumen de exchange</li>
                                        <li>• Direcciones únicas (Usuarios)</li>
                                        <li>• Transacciones diarias (Uso)</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="col-md-4 mb-3">
                                <div class="p-3 border rounded bg-light h-100">
                                    <h5 style="color:#4D4D4D;">2. Infraestructura de Bitcoin</h5>
                                    <p class="small text-muted mb-2">Mide la salud física de la red.</p>
                                    <hr>
                                    <ul class="list-unstyled text-start small ps-3">
                                        <li>• Hashrate (Potencia de calculo de la red)</li>
                                        <li>• Dificultad de minado</li>
                                        <li>• Tamaño de la mempool (Congestión)</li>
                                        <li>• Tamaño promedio de los bloque</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="col-md-4 mb-3">
                                <div class="p-3 border rounded bg-light h-100">
                                    <h5 style="color:#28a745;">3. Seguridad y coste de un ataque</h5>
                                    <p class="small text-muted mb-2">Analiza la sostenibilidad de incentivos para la seguridad.</p>
                                    <hr>
                                    <ul class="list-unstyled text-start small ps-3">
                                        <li>• Coste de un ataque de 51% (USD/h)</li>
                                        <li>• Ingresos de los mineros</li>
                                        <li>• Total fees recaudados (BTC)</li>
                                        <li>• Coste por transacción (Eficiencia)</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="card p-3 mt-3 mb-3 conclusion-box">
                            <h5 class="conclusion-title mb-2">Conclusión: La realidad del coste de ataque</h5>

                            <p class="small text-dark" style="text-align: justify;">
                                Aunque el coste del ataque por hora puede parecer bajo, aproximadamente 1 millon de dolares por hora, unicamente se estan mirando el OpEx (Gastos operativos) o la factura eléctrica.
                            </p>
                            <p class="small text-dark" style="text-align: justify;">
                                Sin embargo, atacar Bitcoin es prácticamente imposible hoy en día debido al CapEx (Inversión de capital), que es la verdadera barrera:
                            </p>

                            <ul class="small ps-3 mb-1 text-dark">
                                <li><strong>Hashrate actual aproximado:</strong> ~1000 Exahashes/segundo.</li>
                                <li><strong>Para el 51% necesitas:</strong> ~510 Exahashes nuevos.</li>
                                <li><strong>Hardware necesario:</strong> Más de 2.5 millones de máquinas de última generación (como el Antminer S21).</li>
                                <li><strong>Coste del Hardware:</strong> > 7.500 Millones de dólares de inversión inicial.</li>
                            </ul>

                            <p class="small mt-2 mb-0 text-dark">
                                <strong>Resumen:</strong> No basta con tener dinero para pagar la luz; necesitas comprar una infraestructura de hardware de miles de millones de dólares antes de poder enchufarla, algo que requiere de una gran inversion inicial y que parece inverosimil desde el punto de vista logístico.
                            </p>
                        </div>

                        <div class="alert alert-secondary mt-3 mb-0 d-flex align-items-center">
                            <div class="flex-grow-1">
                                <strong>Fuentes de datos y procesamiento de los mismos:</strong><br>
                                <span class="small">
                                    Los datos han sido extraídos mediante procesos ETL desde la API pública de <em>Blockchain.com</em>, se han utilizado datos de electricidad de EEUU obtenidos de la <em>U.S. Energy Information Administration (EIA)</em> y se han obtenido datos de la eficiencia minera de <em>https://www.asicminervalue.com/<em>. 
                                    Se han aplicado transformaciones para el cálculo de consumo energético (GW) y costes de ataque basados en la eficiencia media del hardware de minería (J/TH) del periodo seleccionado.
                                </span>
                            </div>
                        </div>

                    </div>
                </div>

                <div class="tab-pane fade" id="tab2">
                    <div class="row">
                        <div class="col-lg-9">
                            <div class="card p-1">{plot_market_html}</div>
                        </div>
                        <div class="col-lg-3">
                            <div class="card p-3 h-100 info-text" style="background-color: #ffffff;">
                                <h3 class="mb-4 border-bottom pb-2">Precio y uso de la red</h3>
                                <h5>1. Precio de mercado</h5>
                                <p>Precio de mercado del Bitcoin en dolares. Es el incentivo principal que atrae a los mineros y da seguridad a la red.</p>
                                <h5>2. Volumen de exchange</h5>
                                <p>Volumne intercambiado en los principales exchanges en dolares. Muestra la liquidez. Valor de todos los bitcoins comprados y vendidos en los principales exchanges durante ese día.</p>
                                <h5>3. Direcciones únicas</h5>
                                <p>Proxy de adopción de usuarios. Cantidad total de direcciones de Bitcoin diferentes que participaron en una transacción durante ese día específico.</p>
                                <h5>4. Transacciones diarias</h5>
                                <p>Medida de uso de la red. Número total de transacciones confirmadas e incluidas en la blockchain de Bitcoin en un dia.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade" id="tab3">
                    <div class="row">
                        <div class="col-lg-9">
                            <div class="card p-1">{plot_infra_html}</div>
                        </div>
                        <div class="col-lg-3">
                            <div class="card p-3 h-100 info-text" style="background-color: #ffffff;">
                                <h3 class="mb-4 border-bottom pb-2">Infraestructura de Bitcoin</h3>
                                <h5>1. Hashrate</h5>
                                <p>La métrica reina de seguridad física. Representa la potencia de cálculo total dedicada a crear un nuevo bloque de Bitcoin.</p>
                                <h5>2. Dificultad de bloque</h5>
                                <p>Valor que representa el numero de calculos necesarios para obtener un nuevo bloque de Bitcoin. Se ajusta de forma automatica cada 2016 bloques para crear un bloque cada 10 minutos.</p>
                                <h5>3. Tamaño de la mempool</h5>
                                <p>La "sala de espera". Si se llena, indica congestión y subida de comisiones de las transacciones ya que las transacciones se priorizan en funcion de la comision que pagan.</p>
                                <h5>4. Tamaño promedio de bloque</h5>
                                <p>Promedio de espacio usado por bloque. Un bloque lleno (~1-2MB) indica máxima demanda de espacio, esta limitado por el algoritmo de Bitcoin.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade" id="tab4">
                    <div class="row">
                        <div class="col-lg-9">
                            <div class="card p-1">{plot_security_html}</div>
                        </div>
                        <div class="col-lg-3">
                            <div class="card p-3 h-100 info-text" style="background-color: #ffffff;">
                                <h3 class="mb-4 border-bottom pb-2">Seguridad y coste de un ataque</h3>
                                <h5>1. Coste de un ataque de 51%</h5>
                                <p>Cuánto costaría en electricidad atacar la red por 1 hora, suponiendo la maxima eficiencia de los mineros y no incluyendo los costes de obtencion de los mineros, unicamente el coste energetico. Si esto sube, BTC es más seguro.</p>
                                <h5>2. Ingresos de los mineros</h5>
                                <p>Dinero total que ganan los mineros en un día. Es la suma del subsidio de bloque + comisiones. Es el presupuesto de seguridad de la red.</p>
                                <h5>3. Total fees recaudados</h5>
                                <p>Cantidad total de Bitcoin pagado en comisiones por los usuarios. Fundamental para la sostenibilidad a largo plazo.</p>
                                <h5>4. Coste por transacción</h5>
                                <p>Ingreso de los mineros entre numero de transacciones diarias. Promedio diario en dolares por transaccion. Tiene en cuenta tambien la creacion de nuevo Bitcoin, por lo que no es el precio promedio que paga el usuario por transaccion.</p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <footer class="text-center py-3 text-muted">UOC - Master en Visualización de Datos | 2025</footer>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Dashboard generado exitosamente en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()