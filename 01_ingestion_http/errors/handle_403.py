from common.http_session import create_session

BASE_URL = "https://httpbin.org"

def run():
    session = create_session()
    response = session.get(f"{BASE_URL}/status/403")

    if response.status_code == 403:
        print("Access denied detected (403). Logging and continuing.")

if __name__ == "__main__":
    run()
