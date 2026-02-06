# Diagrama del Pipeline ETL - Cliente HTTP Automatizado

## Flujo completo del pipeline:

```mermaid
graph TD
    A["🌐 Ingestión HTTP<br/>01_ingestion_http<br/>httpbin.org"] 
    B["📋 Simulación de Logs<br/>02_simulation_logs<br/>generar_datos.py"]
    C["📊 Procesamiento KPIs<br/>03_kpi_processing<br/>calcular_kpis.py"]
    D["🔄 ETL - Pentaho<br/>04_etl_pentaho"]
    E["📈 Reportes<br/>05_reporting<br/>generar_reporte.py"]
    
    F["💾 JSONL<br/>http_logs.jsonl"]
    G["📑 CSV<br/>kpi_por_endpoint_dia.csv"]
    H["🗄️ SQLite<br/>stg_kpi_endpoint_dia<br/>fct_kpi_endpoint_dia"]
    I["🌐 HTML<br/>kpi_diario.html"]
    
    A -->|Simula| B
    B -->|Genera| F
    F -->|Lee| C
    C -->|Calcula| G
    G -->|Entrada CSV| D
    D -->|Carga| H
    G -->|Visualiza| E
    E -->|Genera| I
    H -->|Fuente| E
    
    style A fill:#e1f5ff
    style B fill:#f3e5f5
    style C fill:#e8f5e9
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#f5f5f5
    style G fill:#f5f5f5
    style H fill:#f5f5f5
    style I fill:#f5f5f5
```

## Detalle del flujo ETL (Módulo 04):

```mermaid
graph LR
    CSV["📑 CSV Input<br/>kpi_por_endpoint_dia.csv"]
    
    STEP1["Step 1:<br/>CSV Reader"]
    STEP2["Step 2:<br/>Type Cast"]
    STEP3["Step 3:<br/>Filter Rows<br/>validation"]
    STEP4["Step 4:<br/>Table Output<br/>STG"]
    STEP5["Step 5:<br/>Table Output<br/>FACT"]
    STEP6["Step 6:<br/>Audit Log"]
    
    DB["🗄️ SQLite<br/>three tables"]
    
    CSV --> STEP1
    STEP1 --> STEP2
    STEP2 --> STEP3
    STEP3 --> STEP4
    STEP4 --> STEP5
    STEP5 --> STEP6
    STEP4 --> DB
    STEP5 --> DB
    STEP6 --> DB
    
    style CSV fill:#fff9c4
    style STEP1 fill:#bbdefb
    style STEP2 fill:#c8e6c9
    style STEP3 fill:#ffccbc
    style STEP4 fill:#f8bbd0
    style STEP5 fill:#f8bbd0
    style STEP6 fill:#d1c4e9
    style DB fill:#ffe0b2
```

## Estructura de datos - Tablas SQLite:

```
STG_KPI_ENDPOINT_DIA (Staging)
├─ date_utc (TEXT) ────────────┐
├─ endpoint_base (TEXT) ───────┤─ PRIMARY KEY
├─ requests_total (INTEGER)    │
├─ success_2xx (INTEGER)       │
├─ client_4xx (INTEGER)        │
├─ server_5xx (INTEGER)        │
├─ parse_errors (INTEGER)      │
├─ avg_elapsed_ms (REAL)       │
├─ p90_elapsed_ms (REAL)       │
└─ created_at (TIMESTAMP)      └─ Auditoría

FCT_KPI_ENDPOINT_DIA (Fact Table)
└─ [IDÉNTICA A STG]
   (Copia para análisis independiente)

AUDIT_ETL_LOG (Auditoría)
├─ id (INTEGER) ───────────────────┐
├─ job_name (TEXT)                │─ PRIMARY KEY
├─ execution_date (TIMESTAMP)      │
├─ records_loaded (INTEGER)        │
├─ records_expected (INTEGER)      │
├─ status (TEXT)                   │
├─ error_message (TEXT)            │
└─ duration_seconds (REAL)         └─ Auditoría
```

## Job Pentaho (j_daily_kpi.kjb):

```mermaid
graph TD
    START["▶ INICIO<br/>j_daily_kpi"]
    TRANS["⚙ Ejecutar Transformation<br/>t_load_kpi.ktr"]
    VALIDATE["✓ Validar Registros<br/>success_2xx + client_4xx<br/>+ server_5xx = requests_total"]
    VERIFY["🔍 Table Exists Check<br/>Verificar que tablas<br/>existan en BD"]
    LOG["📝 Write Log<br/>audit_etl_log"]
    SUCCESS["✅ FIN EXITOSO"]
    FAIL["❌ ERROR"]
    
    START --> TRANS
    TRANS --> VALIDATE
    VALIDATE -->|OK| VERIFY
    VALIDATE -->|FAIL| LOG
    LOG --> FAIL
    VERIFY -->|OK| LOG
    VERIFY -->|FAIL| LOG
    LOG -->|Success| SUCCESS
    LOG -->|Fail| FAIL
    
    style START fill:#c8e6c9
    style TRANS fill:#bbdefb
    style VALIDATE fill:#ffccbc
    style VERIFY fill:#f8bbd0
    style LOG fill:#d1c4e9
    style SUCCESS fill:#a5d6a7
    style FAIL fill:#ef9a9a
```

## Pipeline completo - Vista macro:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENTE HTTP AUTOMATIZADO                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  01 - Ingestión  │   │  02 - Simulación │   │  03 - Cálculo    │
│      HTTP        │──→│      de Logs     │──→│      de KPIs      │
│ httpbin.org      │   │ generar_datos.py │   │ calcular_kpis.py │
└──────────────────┘   └──────────────────┘   └──────────────────┘
                                                       │
                          ┌────────────────────────────┼────────────────────────────┐
                          │                            │                            │
                          ▼                            ▼                            ▼
                   ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
                   │  04 - ETL        │       │  05 - Reportes   │       │  Análisis Local  │
                   │    Pentaho       │       │     HTML         │       │     CSV / XML    │
                   └──────────────────┘       └──────────────────┘       └──────────────────┘
                          │
                          ▼
                   ┌──────────────────┐
                   │    SQLite DB     │
                   │  - stg_*         │
                   │  - fct_*         │
                   │  - audit_*       │
                   └──────────────────┘
```

## Componentes del Job ETL:

1. **CSV Input**: Lee `kpi_por_endpoint_dia.csv`
2. **Type Casting**: Convierte strings a tipos correctos (fecha, int, float)
3. **Filter Rows**: Valida que parse_errors + 2xx + 4xx + 5xx = requests_total
4. **Table Output (STG)**: Inserta en stg_kpi_endpoint_dia
5. **Table Output (FCT)**: Inserta en fct_kpi_endpoint_dia
6. **Audit Logger**: Registra resultado en audit_etl_log

## Validaciones del Job:

- ✓ Archivo CSV existe
- ✓ Columnas requeridas presentes
- ✓ Tipos de datos correctos
- ✓ Sanidad de datos (sumas coinciden)
- ✓ Registros cargados = registros esperados
- ✓ Timestamps válidos

## Ejecución del Job:

```bash
# Desde Pentaho Spoon (GUI)
File → Open → j_daily_kpi.kjb → Run

# O desde la línea de comandos
./pdi/sh/kitchen.sh -file=/path/to/j_daily_kpi.kjb
```
