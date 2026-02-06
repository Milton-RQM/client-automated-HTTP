#!/usr/bin/env python3
"""
Script para generar un diagrama visual HTML del pipeline ETL.
Útil para visualizar el flujo completo en un navegador.

Uso:
    python visualizar_pipeline.py --output pipeline_diagram.html
"""

import argparse
from pathlib import Path


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pipeline ETL - Visualización</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px 20px;
        }
        
        .diagram-section {
            margin-bottom: 50px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 5px solid #667eea;
        }
        
        .diagram-section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .diagram-section p {
            color: #555;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .mermaid {
            display: flex;
            justify-content: center;
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            overflow-x: auto;
        }
        
        .module {
            display: inline-block;
            padding: 15px 25px;
            margin: 10px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            text-align: center;
            min-width: 150px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .module-01 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .module-02 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .module-03 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .module-04 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
        .module-05 { background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-top: 4px solid #667eea;
        }
        
        .stat-card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .stat-card p {
            color: #777;
            font-size: 0.95em;
            line-height: 1.6;
        }
        
        footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #777;
            border-top: 1px solid #ddd;
        }
        
        .flow-arrow {
            text-align: center;
            font-size: 2em;
            color: #667eea;
            margin: 10px 0;
        }
        
        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8em;
            }
            
            .content {
                padding: 20px 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔄 Pipeline ETL - Cliente HTTP Automatizado</h1>
            <p>Flujo completo de ingestión, procesamiento y reportes</p>
        </header>
        
        <div class="content">
            <!-- Diagrama 1: Pipeline Completo -->
            <div class="diagram-section">
                <h2>📊 1. Flujo Completo del Pipeline</h2>
                <p>Vista general de cómo los datos fluyen a través de todos los módulos:</p>
                <div class="mermaid">
                    graph LR
                    A["🌐 01<br/>Ingestión HTTP<br/>httpbin.org"] -->|simula| B["📋 02<br/>Simulación<br/>Logs"]
                    B -->|genera| C["📄 Datos JSONL<br/>500 registros"]
                    C -->|procesa| D["📊 03<br/>Cálculo KPIs"]
                    D -->|genera| E["📑 CSV KPIs<br/>por endpoint/día"]
                    E -->|ETL| F["🔄 04<br/>Pentaho<br/>Transformación"]
                    E -->|visualiza| G["📈 05<br/>Reportes HTML"]
                    F -->|carga| H["🗄️ SQLite<br/>stg & fct tables"]
                    H -->|fuente| G
                    G -->|genera| I["🌐 HTML Report<br/>Tablas & Gráficos"]
                    
                    style A fill:#667eea,color:#fff
                    style B fill:#f093fb,color:#fff
                    style D fill:#4facfe,color:#fff
                    style F fill:#fa709a,color:#fff
                    style G fill:#30cfd0,color:#fff
                    style H fill:#764ba2,color:#fff
                    style I fill:#330867,color:#fff
                </div>
            </div>
            
            <!-- Diagrama 2: Transformación ETL -->
            <div class="diagram-section">
                <h2>⚙️ 2. Transformación Pentaho (t_load_kpi.ktr)</h2>
                <p>Pasos de transformación dentro del motor ETL:</p>
                <div class="mermaid">
                    graph TD
                    A["📥 CSV Input<br/>kpi_por_endpoint_dia.csv"] --> B["🔤 Type Casting<br/>string → fecha/int/float"]
                    B --> C["🔍 Filter Rows<br/>Validación de datos"]
                    C -->|OK| D["💾 Table Output<br/>stg_kpi_endpoint_dia"]
                    C -->|OK| E["💾 Table Output<br/>fct_kpi_endpoint_dia"]
                    D --> F["📝 Audit Logger<br/>audit_etl_log"]
                    E --> F
                    F --> G["✅ Carga Completada"]
                    C -->|ERROR| H["❌ Registros Rechazados"]
                    
                    style A fill:#fff3e0,color:#333
                    style B fill:#e3f2fd,color:#333
                    style C fill:#f3e5f5,color:#333
                    style D fill:#e8f5e9,color:#333
                    style E fill:#e8f5e9,color:#333
                    style F fill:#fce4ec,color:#333
                    style G fill:#c8e6c9,color:#333
                    style H fill:#ffcdd2,color:#333
                </div>
            </div>
            
            <!-- Estadísticas -->
            <div class="stats">
                <div class="stat-card">
                    <h3>📦 Módulos</h3>
                    <p><strong>5 módulos independientes:</strong> Ingestión, Simulación, KPIs, ETL, Reportes</p>
                </div>
                <div class="stat-card">
                    <h3>📊 Datos generados</h3>
                    <p><strong>500+ registros</strong> sintéticos por ejecución, con 7–9 métricas por registro</p>
                </div>
                <div class="stat-card">
                    <h3>🗄️ Base de datos</h3>
                    <p><strong>3 tablas SQLite:</strong> staging, fact table, auditoría</p>
                </div>
                <div class="stat-card">
                    <h3>🔄 Flujo ETL</h3>
                    <p><strong>6 pasos:</strong> Input → Type → Filter → Load × 2 → Audit</p>
                </div>
                <div class="stat-card">
                    <h3>📈 KPIs calculados</h3>
                    <p><strong>9 métricas:</strong> Requests, éxitos, errores, latencia, percentil 90</p>
                </div>
                <div class="stat-card">
                    <h3>⏱️ Validaciones</h3>
                    <p><strong>8+ controles:</strong> Integridad, tipos, sumas, archivos, timestamps</p>
                </div>
            </div>
            
            <!-- Diagrama 3: Job Pentaho -->
            <div class="diagram-section">
                <h2>🎯 3. Job Pentaho (j_daily_kpi.kjb)</h2>
                <p>Orquestación y validación del pipeline ETL:</p>
                <div class="mermaid">
                    graph TD
                    A["▶ INICIO<br/>j_daily_kpi"] --> B["⚙️ Ejecutar<br/>t_load_kpi.ktr"]
                    B --> C{¿Éxito?}
                    C -->|SÍ| D["🔍 Validar<br/>Somas de columnas"]
                    C -->|NO| E["❌ ERROR"]
                    D --> F{¿Válido?}
                    F -->|SÍ| G["✓ Verificar<br/>Table Exists"]
                    F -->|NO| E
                    G --> H{¿Existen?}
                    H -->|SÍ| I["📝 Registrar en<br/>audit_etl_log"]
                    H -->|NO| E
                    I --> J["✅ ÉXITO"]
                    E --> K["📝 Registrar<br/>error"]
                    K --> L["❌ FIN CON ERROR"]
                    
                    style A fill:#c8e6c9
                    style B fill:#bbdefb
                    style J fill:#a5d6a7
                    style L fill:#ef9a9a
                </div>
            </div>
            
            <!-- Módulos -->
            <div class="diagram-section">
                <h2>📦 Módulos del Proyecto</h2>
                <p>Cada módulo tiene una responsabilidad clara y puede ejecutarse independientemente:</p>
                <div style="text-align: center;">
                    <div class="module module-01">
                        01 - Ingestión HTTP<br/>
                        <small>httpbin.org</small>
                    </div>
                    <div class="flow-arrow">↓</div>
                    <div class="module module-02">
                        02 - Simulación<br/>
                        <small>generar_datos.py</small>
                    </div>
                    <div class="flow-arrow">↓</div>
                    <div class="module module-03">
                        03 - KPIs<br/>
                        <small>calcular_kpis.py</small>
                    </div>
                    <div class="flow-arrow">↓↓</div>
                    <div>
                        <div class="module module-04" style="display: inline-block; margin-right: 20px;">
                            04 - ETL<br/>
                            <small>Pentaho</small>
                        </div>
                        <div class="module module-05" style="display: inline-block;">
                            05 - Reportes<br/>
                            <small>generar_reporte.py</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Checklist -->
            <div class="diagram-section">
                <h2>✅ Checklist de Ejecución</h2>
                <p style="margin-bottom: 20px;">Pasos para ejecutar el pipeline completo:</p>
                <div style="background: white; padding: 20px; border-radius: 8px;">
                    <ol style="line-height: 2.5; color: #555;">
                        <li>✓ Instalar dependencias: <code>pip install -r requirements.txt</code></li>
                        <li>✓ Validar ambiente: <code>python setup_and_validate.py</code></li>
                        <li>✓ Generar datos: <code>python 02_simulation_logs/generar_datos.py</code></li>
                        <li>✓ Calcular KPIs: <code>python 03_kpi_processing/calcular_kpis.py</code></li>
                        <li>✓ (Opcional) Ejecutar ETL: Pentaho GUI o CLI</li>
                        <li>✓ Generar reporte: <code>python 05_reporting/generar_reporte.py</code></li>
                        <li>✓ Ver resultado: Abrir HTML en navegador</li>
                    </ol>
                </div>
            </div>
        </div>
        
        <footer>
            <p>📊 Pipeline de Ingestión HTTP, Procesamiento de KPIs y ETL</p>
            <p>Proyecto de Data Engineering • 2026</p>
            <p>
                <a href="https://github.com/Milton-RQM/client-automated-HTTP" 
                   style="color: #667eea; text-decoration: none;">
                   Repositorio en GitHub →
                </a>
            </p>
        </footer>
    </div>
    
    <script>
        mermaid.initialize({ startOnLoad: true, theme: 'default' });
        mermaid.contentLoaded();
    </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Genera un diagrama visual HTML del pipeline ETL"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="pipeline_diagram.html",
        help="Ruta del archivo HTML de salida (default: pipeline_diagram.html)"
    )
    
    args = parser.parse_args()
    output_path = Path(args.output)
    
    # Crear directorio si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Escribir el archivo HTML
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    
    print(f"✅ Diagrama generado: {output_path.resolve()}")
    print(f"\n📖 Abre el archivo en tu navegador para ver el diagrama interactivo")
    
    # Intentar abrir en navegador automáticamente
    import webbrowser
    import sys
    
    try:
        if sys.platform == 'win32':
            import os
            os.startfile(str(output_path.resolve()))
        elif sys.platform == 'darwin':  # macOS
            import os
            os.system(f'open "{output_path.resolve()}"')
        else:  # Linux
            import webbrowser
            webbrowser.open(f'file://{output_path.resolve()}')
        print("🌐 Abriendo en navegador...")
    except Exception as e:
        print(f"⚠️ No se pudo abrir automáticamente: {e}")
        print(f"   Abre manualmente: {output_path.resolve()}")


if __name__ == "__main__":
    main()
