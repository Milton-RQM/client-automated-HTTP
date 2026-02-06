from pathlib import Path
from lxml import etree
from common.http_session import create_session

BASE_URL = "https://httpbin.org"
OUTPUT_DIR = Path("outputs/xml")

def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    session = create_session()

    response = session.get(f"{BASE_URL}/xml")
    root = etree.fromstring(response.content)

    with open(OUTPUT_DIR / "response.xml", "wb") as f:
        f.write(etree.tostring(root, pretty_print=True))

    print("XML saved successfully")

if __name__ == "__main__":
    run()
