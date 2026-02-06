from common.http_session import create_session

BASE_URL = "https://httpbin.org"

def run():
    session = create_session()

    session.get(f"{BASE_URL}/cookies/set?session=active")
    response = session.get(f"{BASE_URL}/cookies")

    print("Cookies:", response.json())

if __name__ == "__main__":
    run()
