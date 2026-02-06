import pandas as pd
import matplotlib.pyplot as plt
import argparse
import base64
from io import BytesIO
from pathlib import Path
from datetime import datetime

def fig_to_base64(fig):
    """Convierte gráficos de matplotlib a base64 para evitar depender de archivos externos."""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generar_html(df, plots_base64, stats, output_path, umbral, autor):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    rows_html = ""
    # Seleccionamos el Top 10 para la tabla de detalles
    top_10 = df.sort_values('requests_total', ascending=False).head(10)
    
    for _, row in top_10.iterrows():
        success_pct = (row['success_2xx'] / row['requests_total'] * 100)
        # Alerta roja si supera el umbral P90
        p90_style = 'style="color: #e74c3c; font-weight: bold;"' if row['p90_elapsed_ms'] > umbral else ""
        
        rows_html += f"""
        <tr>
            <td>{row['endpoint_base']}</td>
            <td>{row['requests_total']:,}</td>
            <td>{success_pct:.1f}%</td>
            <td>{row['avg_elapsed_ms']:.2f}ms</td>
            <td {p90_style}>{row['p90_elapsed_ms']:.2f}ms</td>
        </tr>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard KPI - {now}</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 40px; }}
            .header {{ 
                background-color: #2c3e50; color: white; padding: 30px; border-radius: 8px 8px 0 0; 
                position: relative; text-align: center; border-bottom: 4px solid #3498db;
            }}
            .logo-placeholder {{ position: absolute; top: 25px; left: 30px; font-weight: bold; font-size: 1.2em; color: #3498db; border: 2px solid #3498db; padding: 5px 10px; border-radius: 4px; }}
            .header h1 {{ margin: 0; font-size: 26px; text-transform: uppercase; letter-spacing: 2px; }}
            .header .subtitle {{ margin-top: 10px; font-size: 0.95em; color: #bdc3c7; }}
            .header .date-top {{ position: absolute; top: 15px; right: 25px; font-size: 0.85em; color: #ecf0f1; }}
            
            .stats-container {{ display: flex; justify-content: space-between; margin: 25px 0; gap: 20px; }}
            .stat-card {{ 
                background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                flex: 1; text-align: center; transition: transform 0.2s;
            }}
            .stat-card:hover {{ transform: translateY(-5px); }}
            .stat-card h3 {{ margin: 0; color: #7f8c8d; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; }}
            .stat-card p {{ font-size: 2em; margin: 10px 0; font-weight: bold; color: #2c3e50; }}
            
            .grid-plots {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-top: 25px; }}
            .plot-box {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }}
            .plot-box img {{ max-width: 100%; height: auto; border-radius: 4px; }}
            
            .table-section {{ background: white; padding: 30px; border-radius: 8px; margin-top: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h2 {{ color: #2c3e50; border-left: 5px solid #3498db; padding-left: 15px; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 15px; border-bottom: 1px solid #eee; text-align: left; }}
            th {{ background-color: #f8f9fa; color: #34495e; font-weight: 600; text-transform: uppercase; font-size: 0.85em; }}
            tr:hover {{ background-color: #f9f9f9; }}
            
            .footer {{ margin-top: 50px; padding: 20px 0; border-top: 2px solid #ddd; font-size: 0.9em; color: #7f8c8d; }}
            .footer .author {{ float: left; font-style: italic; }}
            .footer .brand {{ float: right; font-weight: bold; color: #2c3e50; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo-placeholder">DATA API</div>
            <div class="date-top">Fecha de reporte: {now}</div>
            <h1>Resumen Diario de KPIs - Servicios API</h1>
            <div class="subtitle">Última actualización: {now} (Zona Horaria Local)</div>
        </div>
        
        <div class="stats-container">
            <div class="stat-card"><h3>Total Solicitudes</h3><p>{stats['total_req']:,}</p></div>
            <div class="stat-card"><h3>Tasa Éxito (2xx)</h3><p>{stats['success_rate']:.2f}%</p></div>
            <div class="stat-card"><h3>Global P90</h3><p>{stats['global_p90']:.1f} ms</p></div>
            <div class="stat-card"><h3>Total Incidencias</h3><p>{stats['total_err']:,}</p></div>
        </div>

        <div class="grid-plots">
            <div class="plot-box"><h3>Volumen por Servicio</h3><img src="data:image/png;base64,{plots_base64[0]}"></div>
            <div class="plot-box"><h3>Latencia P90 vs Límite</h3><img src="data:image/png;base64,{plots_base64[1]}"></div>
            <div class="plot-box"><h3>Distribución de Errores</h3><img src="data:image/png;base64,{plots_base64[2]}"></div>
            <div class="plot-box"><h3>Dispersión de Respuestas</h3><img src="data:image/png;base64,{plots_base64[3]}"></div>
        </div>

        <div class="table-section">
            <h2>Detalle Top 10 Endpoints Criticos</h2>
            <table>
                <thead>
                    <tr><th>Endpoint Base</th><th>Total Requests</th><th>% Éxito</th><th>Promedio (Avg)</th><th>Percentil 90 (P90)</th></tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>

        <div class="footer">
            <div class="author">Autor: {autor}</div>
            <div class="brand">Pentaho Data Integration - Python Reporting Module</div>
            <div style="clear: both;"></div>
        </div>
    </body>
    </html>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)

def main():
    parser = argparse.ArgumentParser()
    # Rutas actualizadas según tu estructura de carpetas
    parser.add_argument("--input", default="03_kpi_processing/out/kpi_por_endpoint_dia.csv")
    parser.add_argument("--output", default="05_reporting/out/report/kpi_diario.html")
    parser.add_argument("--umbral_p90", type=float, default=300.0)
    parser.add_argument("--autor", default="Milton Quiñonez") 
    args = parser.parse_args()

    # Verificación de Carpeta de Salida
    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not Path(args.input).exists():
        print(f"Error: No se encontró el archivo {args.input}")
        return

    df = pd.read_csv(args.input)
    
    # Cálculos globales para los cuadros superiores
    stats = {
        'total_req': df['requests_total'].sum(),
        'success_rate': (df['success_2xx'].sum() / df['requests_total'].sum() * 100),
        'global_p90': df['p90_elapsed_ms'].mean(),
        'total_err': df['client_4xx'].sum() + df['server_5xx'].sum()
    }

    # Configuración de estilo para los gráficos
    plt.style.use('ggplot')
    plots = []
    
    # 1. Gráfico de Barras: Volumen
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    df.sort_values('requests_total').tail(10).plot.barh(x='endpoint_base', y='requests_total', ax=ax1, color='#2c3e50')
    ax1.set_title("Volumen por Endpoint", fontsize=10)
    plots.append(fig_to_base64(fig1))

    # 2. Gráfico de Barras: P90 vs Umbral
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    df.head(10).plot.bar(x='endpoint_base', y='p90_elapsed_ms', ax=ax2, color='#3498db')
    ax2.axhline(y=args.umbral_p90, color='#e74c3c', linestyle='--', label='Umbral')
    ax2.set_title("Performance P90 (ms)", fontsize=10)
    plots.append(fig_to_base64(fig2))

    # 3. Gráfico Circular: Proporción Global
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.pie([df['success_2xx'].sum(), df['client_4xx'].sum(), df['server_5xx'].sum()], 
            labels=['Ok', 'Client Err', 'Server Err'], autopct='%1.1f%%', colors=['#27ae60', '#f1c40f', '#e74c3c'])
    plots.append(fig_to_base64(fig3))

    # 4. Histograma/Boxplot de Latencias
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    ax4.boxplot(df['p90_elapsed_ms'], vert=False)
    ax4.set_title("Distribución de Latencias P90", fontsize=10)
    plots.append(fig_to_base64(fig4))

    generar_html(df, plots, stats, args.output, args.umbral_p90, args.autor)
    print(f"Reporte generado con éxito en: {args.output}")

if __name__ == "__main__":
    main()