import json
import argparse
import re
from pathlib import Path
import pandas as pd
import numpy as np


DEFAULT_INPUT = Path("02_simulation_logs/out/http_logs.jsonl")
OUT_DIR = Path("out")
OUT_CSV = OUT_DIR / "kpi_por_endpoint_dia.csv"


def normalize_endpoint(endpoint: str) -> str:
    """
    Normaliza una ruta de endpoint eliminando parámetros y valores numéricos variables.
    
    Ejemplos:
    - "/status/403" → "/status"
    - "/users/123" → "/users"
    - "/api/v1/endpoints?param=value&id=456" → "/api/v1/endpoints"
    - "/resource/abc-123-def" → "/resource"
    
    Estrategia:
    1. Elimina query strings (después de "?")
    2. Reemplaza segmentos puramente numéricos por patrón genérico
    3. Reemplaza segmentos que contienen "ids", "keys", hashes (alphanuméricas con guiones)
    """
    # Eliminar query string
    endpoint = endpoint.split("?")[0]
    
    # Dividir en segmentos
    parts = endpoint.split("/")
    normalized_parts = []
    
    for part in parts:
        if not part:
            normalized_parts.append(part)
        # Si es numérico puro, omitir (es un parámetro variable)
        elif re.match(r'^\d+$', part):
            continue
        # Si contiene UUID, ID o hash-like (alphanuméricas con guiones), omitir
        elif re.match(r'^[a-zA-Z0-9\-]{8,}$', part):
            continue
        else:
            normalized_parts.append(part)
    
    # Reconstruir la ruta
    result = "/".join(normalized_parts)
    return result if result else "/"


def load_jsonl(path: Path) -> pd.DataFrame:
    """
    Carga un archivo JSONL y retorna un DataFrame de pandas.
    Valida que cada línea sea JSON válido.
    """
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON mal formado en línea {line_num}: {e}")
    return pd.DataFrame(rows)


def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula KPIs diarios por endpoint normalizado.
    
    Procesa:
    - Conversión de timestamps
    - Normalización de endpoints
    - Validación de parse_result
    - Clasificación de status codes
    - Agrupación y agregación de métricas
    """
    # Normalizaciones
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce", utc=True)
    df["date_utc"] = df["timestamp_utc"].dt.date
    df["elapsed_ms"] = pd.to_numeric(df["elapsed_ms"], errors="coerce")
    
    # Normalizar endpoint: quitar parámetros y IDs numéricos
    df["endpoint_base"] = df["endpoint"].apply(normalize_endpoint)
    
    # Clasificación de status codes
    df["is_2xx"] = df["status_code"].between(200, 299)
    df["is_4xx"] = df["status_code"].between(400, 499)
    df["is_5xx"] = df["status_code"].between(500, 599)
    
    # parse_errors: registros donde parse_result != "ok"
    # Si la columna no existe, asumimos que todos son válidos
    if "parse_result" in df.columns:
        df["is_parse_error"] = df["parse_result"] != "ok"
    else:
        df["is_parse_error"] = False

    # Agrupación por día + endpoint_base
    g = df.groupby(["date_utc", "endpoint_base"], as_index=False)

    # Función auxiliar para calcular percentil 90 usando numpy
    def p90(x):
        return np.percentile(x.dropna(), 90) if len(x.dropna()) > 0 else 0

    kpi = g.agg(
        requests_total=("status_code", "count"),
        success_2xx=("is_2xx", "sum"),
        client_4xx=("is_4xx", "sum"),
        server_5xx=("is_5xx", "sum"),
        parse_errors=("is_parse_error", "sum"),
        avg_elapsed_ms=("elapsed_ms", "mean"),
        p90_elapsed_ms=("elapsed_ms", p90),
    )

    # Convertir a int las columnas de conteo
    kpi[["success_2xx", "client_4xx", "server_5xx", "parse_errors"]] = \
        kpi[["success_2xx", "client_4xx", "server_5xx", "parse_errors"]].astype(int)
    
    # Redondeos para promedios
    kpi["avg_elapsed_ms"] = kpi["avg_elapsed_ms"].round(2)
    kpi["p90_elapsed_ms"] = kpi["p90_elapsed_ms"].round(2)

    # Orden final
    kpi = kpi.sort_values(["date_utc", "endpoint_base"]).reset_index(drop=True)
    return kpi


def main(input_path: Path, output_path: Path):
    """
    Función principal.
    
    Args:
        input_path: Ruta del archivo JSONL de entrada (out/datos.jsonl)
        output_path: Ruta del archivo CSV de salida (out/kpi_por_endpoint_dia.csv)
    """
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el input JSONL: {input_path.resolve()}")

    print(f"📖 Leyendo: {input_path.resolve()}")
    df = load_jsonl(input_path)
    print(f"✅ {len(df)} registros cargados")

    # Validar columnas requeridas
    required = {"timestamp_utc", "endpoint", "status_code", "elapsed_ms"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en logs: {sorted(missing)}. Columnas actuales: {list(df.columns)}")

    print(f"📊 Procesando KPIs...")
    kpis = compute_kpis(df)

    # Crear directorio de salida
    output_path.parent.mkdir(parents=True, exist_ok=True)
    kpis.to_csv(output_path, index=False)

    print(f"✅ KPIs generados: {output_path.resolve()}")
    print(f"✅ Filas: {len(kpis)} (agrupado por date_utc + endpoint_base)")
    print(f"\nPrimeras 5 filas:")
    print(kpis.head())



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calcular KPIs diarios desde datos JSONL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python calcular_kpis.py
  python calcular_kpis.py --input out/datos.jsonl --output out/kpi_por_endpoint_dia.csv
  python calcular_kpis.py --input /ruta/logs.jsonl --output /ruta/output.csv
  python 03_kpi_processing/calcular_kpis.py --input 02_simulation_logs/out/http_logs.jsonl --output 03_kpi_processing/out/kpi_por_endpoint_dia.csv 
        """
    )
    parser.add_argument(
        "--input", 
        type=str, 
        default=str(DEFAULT_INPUT), 
        help=f"Ruta del archivo JSONL de entrada (default: {DEFAULT_INPUT})"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default=str(OUT_CSV), 
        help=f"Ruta del archivo CSV de salida (default: {OUT_CSV})"
    )
    
    args = parser.parse_args()
    
    try:
        main(Path(args.input), Path(args.output))
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)



