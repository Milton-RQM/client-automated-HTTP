import json
import random
import argparse
from pathlib import Path
from faker import Faker
from datetime import timezone

# -----------------------------
# Configuración por defecto
# -----------------------------
DEFAULT_ROWS = 500
DEFAULT_SEED = 42

ENDPOINTS = [
    "/get",
    "/post",
    "/xml",
    "/html",
    "/status/403",
    "/redirect"
]

HTTP_METHODS = ["GET", "POST"]

STATUS_DISTRIBUTION = [
    (200, 0.75),
    (400, 0.10),
    (403, 0.05),
    (500, 0.10)
]

OUTPUT_DIR = Path("out")
OUTPUT_FILE = OUTPUT_DIR / "http_logs.jsonl"

# -----------------------------
# Funciones auxiliares
# -----------------------------
def weighted_status():
    r = random.random()
    cumulative = 0.0
    for status, weight in STATUS_DISTRIBUTION:
        cumulative += weight
        if r <= cumulative:
            return status
    return 200


def generate_log(fake):
    status = weighted_status()

    return {
        "timestamp_utc": fake.date_time_this_month(
            tzinfo=timezone.utc
        ).isoformat(),
        "endpoint": random.choice(ENDPOINTS),
        "http_method": random.choice(HTTP_METHODS),
        "status_code": status,
        "elapsed_ms": round(random.uniform(50, 1500), 2),
        "parse_result": "ok" if status == 200 else "error",
        "user_agent": fake.user_agent()
    }

# -----------------------------
# Ejecución principal
# -----------------------------
def main(rows, seed):
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for _ in range(rows):
            log = generate_log(fake)
            f.write(json.dumps(log) + "\n")

    print(f"✔ {rows} logs generados en {OUTPUT_FILE}")
    print(f"✔ Seed utilizada: {seed}")

# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulador de logs HTTP técnicos"
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help="Número de registros a generar"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Semilla para reproducibilidad"
    )

    args = parser.parse_args()

    main(args.rows, args.seed)
