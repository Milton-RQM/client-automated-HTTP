-- =============================================================================
-- SQL Schema para Base de Datos SQLite - Pipeline de KPIs
-- Fecha: 2026-02-06
-- Version: 1.0
-- =============================================================================

-- Tabla de Staging: Carga directa desde CSV
-- Contiene los datos tal como vienen del procesamiento de KPIs
CREATE TABLE IF NOT EXISTS stg_kpi_endpoint_dia (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_utc TEXT NOT NULL,
  endpoint_base TEXT NOT NULL,
  requests_total INTEGER NOT NULL CHECK(requests_total >= 0),
  success_2xx INTEGER DEFAULT 0 CHECK(success_2xx >= 0),
  client_4xx INTEGER DEFAULT 0 CHECK(client_4xx >= 0),
  server_5xx INTEGER DEFAULT 0 CHECK(server_5xx >= 0),
  parse_errors INTEGER DEFAULT 0 CHECK(parse_errors >= 0),
  avg_elapsed_ms REAL DEFAULT 0.0,
  p90_elapsed_ms REAL DEFAULT 0.0,
  loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(date_utc, endpoint_base)
);

-- Indices para staging
CREATE INDEX IF NOT EXISTS idx_stg_date ON stg_kpi_endpoint_dia(date_utc);
CREATE INDEX IF NOT EXISTS idx_stg_endpoint ON stg_kpi_endpoint_dia(endpoint_base);
CREATE INDEX IF NOT EXISTS idx_stg_loaded_at ON stg_kpi_endpoint_dia(loaded_at);

-- Tabla Fact: Para analisis y reportes
-- Replica de staging, pero estructurada para consultas analíticas
CREATE TABLE IF NOT EXISTS fct_kpi_endpoint_dia (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_utc TEXT NOT NULL,
  endpoint_base TEXT NOT NULL,
  requests_total INTEGER NOT NULL CHECK(requests_total >= 0),
  success_2xx INTEGER DEFAULT 0 CHECK(success_2xx >= 0),
  client_4xx INTEGER DEFAULT 0 CHECK(client_4xx >= 0),
  server_5xx INTEGER DEFAULT 0 CHECK(server_5xx >= 0),
  parse_errors INTEGER DEFAULT 0 CHECK(parse_errors >= 0),
  avg_elapsed_ms REAL DEFAULT 0.0,
  p90_elapsed_ms REAL DEFAULT 0.0,
  loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(date_utc, endpoint_base)
);

-- Indices para fact table
CREATE INDEX IF NOT EXISTS idx_fct_date ON fct_kpi_endpoint_dia(date_utc);
CREATE INDEX IF NOT EXISTS idx_fct_endpoint ON fct_kpi_endpoint_dia(endpoint_base);
CREATE INDEX IF NOT EXISTS idx_fct_loaded_at ON fct_kpi_endpoint_dia(loaded_at);

-- Tabla de Auditoria: Registra ejecuciones del ETL
-- Permite rastrear qué se cargó, cuándo y si hubo errores
CREATE TABLE IF NOT EXISTS audit_etl_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_name TEXT NOT NULL,
  transformation_name TEXT,
  execution_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  execution_end TIMESTAMP,
  status TEXT CHECK(status IN ('SUCCESS', 'FAILED', 'PARTIAL')),
  records_processed INTEGER DEFAULT 0,
  records_inserted INTEGER DEFAULT 0,
  records_updated INTEGER DEFAULT 0,
  records_rejected INTEGER DEFAULT 0,
  error_message TEXT,
  duration_seconds REAL,
  executed_by TEXT DEFAULT 'system'
);

-- Indices para auditoria
CREATE INDEX IF NOT EXISTS idx_audit_job ON audit_etl_log(job_name);
CREATE INDEX IF NOT EXISTS idx_audit_status ON audit_etl_log(status);
CREATE INDEX IF NOT EXISTS idx_audit_execution_start ON audit_etl_log(execution_start);

-- Vista: Resumen diario de KPIs por fecha
CREATE VIEW IF NOT EXISTS vw_kpi_resumen_diario AS
SELECT 
  date_utc,
  COUNT(DISTINCT endpoint_base) as num_endpoints,
  SUM(requests_total) as total_requests_dia,
  SUM(success_2xx) as total_success_2xx,
  SUM(client_4xx) as total_client_4xx,
  SUM(server_5xx) as total_server_5xx,
  SUM(parse_errors) as total_parse_errors,
  ROUND(AVG(avg_elapsed_ms), 2) as promedio_latencia,
  MAX(p90_elapsed_ms) as max_p90_latencia
FROM fct_kpi_endpoint_dia
GROUP BY date_utc
ORDER BY date_utc DESC;

-- Vista: KPIs por endpoint (últimas 30 días)
CREATE VIEW IF NOT EXISTS vw_kpi_por_endpoint AS
SELECT 
  endpoint_base,
  COUNT(DISTINCT date_utc) as dias_data,
  SUM(requests_total) as total_requests,
  SUM(success_2xx) as total_success,
  ROUND(100.0 * SUM(success_2xx) / SUM(requests_total), 2) as success_rate_pct,
  ROUND(AVG(avg_elapsed_ms), 2) as avg_latencia,
  ROUND(AVG(p90_elapsed_ms), 2) as avg_p90_latencia
FROM fct_kpi_endpoint_dia
WHERE date(loaded_at) >= date('now', '-30 days')
GROUP BY endpoint_base
ORDER BY total_requests DESC;

-- Vista: Alertas de rendimiento
CREATE VIEW IF NOT EXISTS vw_alertas_rendimiento AS
SELECT 
  date_utc,
  endpoint_base,
  p90_elapsed_ms,
  CASE 
    WHEN p90_elapsed_ms > 500 THEN 'CRITICO'
    WHEN p90_elapsed_ms > 300 THEN 'WARNING'
    ELSE 'OK'
  END as nivel_alerta,
  success_2xx,
  client_4xx + server_5xx as total_errores,
  ROUND(100.0 * (client_4xx + server_5xx) / requests_total, 2) as error_rate_pct
FROM fct_kpi_endpoint_dia
WHERE (p90_elapsed_ms > 300 OR (client_4xx + server_5xx) > requests_total * 0.1)
ORDER BY date_utc DESC, p90_elapsed_ms DESC;

-- =============================================================================
-- SCRIPTS DE VALIDACION
-- =============================================================================

-- Para verificar que las tablas se crearon correctamente:
-- SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- Para listar todas las vistas:
-- SELECT name FROM sqlite_master WHERE type='view' ORDER BY name;

-- Para ver el esquema de una tabla:
-- PRAGMA table_info(fct_kpi_endpoint_dia);
