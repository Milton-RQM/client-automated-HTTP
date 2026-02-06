import json
import argparse
from pathlib import Path
import pandas as pd


DEFAULT_INPUT = Path("../01_ingestion_http/out/http_logs.jsonl")
OUT_DIR = Path("out")
OUT_CSV = OUT_DIR / "kpi_por_endpoint_dia.csv"


def load_jsonl(path: Path) -> pd.DataFrame:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return pd.DataFrame(rows)


def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    # Normalizaciones
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce", utc=True)
    df["date"] = df["timestamp_utc"].dt.date
    df["elapsed_ms"] = pd.to_numeric(df["elapsed_ms"], errors="coerce")

    # Clasificación de status codes
    df["is_2xx"] = df["status_code"].between(200, 299)
    df["is_4xx"] = df["status_code"].between(400, 499)
    df["is_5xx"] = df["status_code"].between(500, 599)

    # Agrupación por día + endpoint
    g = df.groupby(["date", "endpoint"], as_index=False)

    kpi = g.agg(
        total_requests=("status_code", "count"),
        success_2xx=("is_2xx", "sum"),
        errors_4xx=("is_4xx", "sum"),
        errors_5xx=("is_5xx", "sum"),
        avg_elapsed_ms=("elapsed_ms", "mean"),
        p90_elapsed_ms=("elapsed_ms", lambda x: x.quantile(0.90)),
    )

    # Redondeos
    kpi["avg_elapsed_ms"] = kpi["avg_elapsed_ms"].round(2)
    kpi["p90_elapsed_ms"] = kpi["p90_elapsed_ms"].round(2)

    # Orden final
    kpi = kpi.sort_values(["date", "endpoint"]).reset_index(drop=True)
    return kpi


def main(input_path: Path):
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el input JSONL: {input_path.resolve()}")

    df = load_jsonl(input_path)

    required = {"timestamp_utc", "endpoint", "status_code", "elapsed_ms"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en logs: {sorted(missing)}. Columnas actuales: {list(df.columns)}")

    kpis = compute_kpis(df)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    kpis.to_csv(OUT_CSV, index=False)

    print(f"✅ KPIs generados: {OUT_CSV.resolve()}")
    print(f"✅ Filas: {len(kpis)} (agrupado por date + endpoint)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcular KPIs desde logs JSONL")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT), help="Ruta del archivo http_logs.jsonl")
    args = parser.parse_args()

    main(Path(args.input))
