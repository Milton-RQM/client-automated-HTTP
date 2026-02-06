from pathlib import Path
from bs4 import BeautifulSoup
from common.http_session import create_session

BASE_URL = "https://httpbin.org"
OUTPUT_DIR = Path("outputs/html")

def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    session = create_session()

    response = session.get(f"{BASE_URL}/html")
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text

    with open(OUTPUT_DIR / "title.txt", "w", encoding="utf-8") as f:
        f.write(title)

    print("HTML content extracted")

if __name__ == "__main__":
    run()
