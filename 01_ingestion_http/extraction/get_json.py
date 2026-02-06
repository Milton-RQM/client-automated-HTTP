import json
from pathlib import Path
from common.http_session import create_session

BASE_URL = "https://httpbin.org"
OUTPUT_DIR = Path("outputs/json")

def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    session = create_session()

    response = session.get(f"{BASE_URL}/get")

    with open(OUTPUT_DIR / "response.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=2)

    print("JSON saved successfully")

if __name__ == "__main__":
    run()
