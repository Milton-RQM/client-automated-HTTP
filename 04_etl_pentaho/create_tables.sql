-- ============================================================================
-- Script de creación de tablas para el pipeline de KPIs
-- Base de datos: SQLite
-- ============================================================================

-- Tabla de staging: copia directa de los datos procesados
CREATE TABLE IF NOT EXISTS stg_kpi_endpoint_dia (
  date_utc TEXT NOT NULL,
  endpoint_base TEXT NOT NULL,
  requests_total INTEGER NOT NULL,
  success_2xx INTEGER NOT NULL,
  client_4xx INTEGER NOT NULL,
  server_5xx INTEGER NOT NULL,
  parse_errors INTEGER NOT NULL,
  avg_elapsed_ms REAL NOT NULL,
  p90_elapsed_ms REAL NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (date_utc, endpoint_base)
);

-- Tabla de hechos (fact table): copia de staging para análisis
CREATE TABLE IF NOT EXISTS fct_kpi_endpoint_dia (
  date_utc TEXT NOT NULL,
  endpoint_base TEXT NOT NULL,
  requests_total INTEGER NOT NULL,
  success_2xx INTEGER NOT NULL,
  client_4xx INTEGER NOT NULL,
  server_5xx INTEGER NOT NULL,
  parse_errors INTEGER NOT NULL,
  avg_elapsed_ms REAL NOT NULL,
  p90_elapsed_ms REAL NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (date_utc, endpoint_base)
);

-- Tabla de auditoría: registra cada carga ETL
CREATE TABLE IF NOT EXISTS audit_etl_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_name TEXT NOT NULL,
  execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  records_loaded INTEGER,
  records_expected INTEGER,
  status TEXT,
  error_message TEXT,
  duration_seconds REAL
);

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_stg_date ON stg_kpi_endpoint_dia(date_utc);
CREATE INDEX IF NOT EXISTS idx_stg_endpoint ON stg_kpi_endpoint_dia(endpoint_base);
CREATE INDEX IF NOT EXISTS idx_fct_date ON fct_kpi_endpoint_dia(date_utc);
CREATE INDEX IF NOT EXISTS idx_fct_endpoint ON fct_kpi_endpoint_dia(endpoint_base);
CREATE INDEX IF NOT EXISTS idx_audit_job ON audit_etl_log(job_name);

-- ============================================================================
-- Vistas de análisis
-- ============================================================================

-- Vista: Resumen por endpoint
CREATE VIEW IF NOT EXISTS v_kpi_por_endpoint AS
SELECT 
  endpoint_base,
  COUNT(DISTINCT date_utc) as dias,
  SUM(requests_total) as total_requests,
  SUM(success_2xx) as total_success,
  SUM(client_4xx) as total_client_errors,
  SUM(server_5xx) as total_server_errors,
  AVG(avg_elapsed_ms) as avg_response_time,
  MAX(p90_elapsed_ms) as max_p90
FROM fct_kpi_endpoint_dia
GROUP BY endpoint_base
ORDER BY total_requests DESC;

-- Vista: Resumen diario global
CREATE VIEW IF NOT EXISTS v_kpi_diario_global AS
SELECT 
  date_utc,
  COUNT(DISTINCT endpoint_base) as endpoints_monitoreados,
  SUM(requests_total) as total_requests,
  SUM(success_2xx) as total_success,
  SUM(client_4xx) as total_client_errors,
  SUM(server_5xx) as total_server_errors,
  ROUND(AVG(avg_elapsed_ms), 2) as avg_response_time,
  ROUND(AVG(p90_elapsed_ms), 2) as avg_p90
FROM fct_kpi_endpoint_dia
GROUP BY date_utc
ORDER BY date_utc DESC;

-- Vista: Alertas - Endpoints con latencia alta
CREATE VIEW IF NOT EXISTS v_alertas_latencia_alta AS
SELECT 
  date_utc,
  endpoint_base,
  avg_elapsed_ms,
  p90_elapsed_ms,
  CASE 
    WHEN p90_elapsed_ms > 500 THEN 'CRÍTICO'
    WHEN p90_elapsed_ms > 300 THEN 'ALTO'
    ELSE 'NORMAL'
  END as nivel_alerta
FROM fct_kpi_endpoint_dia
WHERE p90_elapsed_ms > 300
ORDER BY p90_elapsed_ms DESC;

-- ============================================================================
-- Stored Procedures / Funciones (para PostgreSQL/MySQL, adaptar para SQLite)
-- ============================================================================

-- En SQLite usamos triggers en lugar de procedures

-- Trigger: Auditar inserciones en fact table
CREATE TRIGGER IF NOT EXISTS trg_audit_fct_insert
AFTER INSERT ON fct_kpi_endpoint_dia
BEGIN
  INSERT INTO audit_etl_log (
    job_name, 
    records_loaded, 
    status, 
    execution_date
  ) 
  VALUES (
    'j_daily_kpi', 
    1, 
    'SUCCESS',
    CURRENT_TIMESTAMP
  );
END;

-- ============================================================================
-- Datos de prueba (opcional, comentar si no es necesario)
-- ============================================================================

-- INSERT INTO stg_kpi_endpoint_dia VALUES
-- ('2026-02-06', '/api', 150, 140, 8, 2, 0, 125.30, 250.45, CURRENT_TIMESTAMP),
-- ('2026-02-06', '/status', 100, 95, 5, 0, 3, 89.20, 180.50, CURRENT_TIMESTAMP);

-- INSERT INTO fct_kpi_endpoint_dia 
-- SELECT * FROM stg_kpi_endpoint_dia;
