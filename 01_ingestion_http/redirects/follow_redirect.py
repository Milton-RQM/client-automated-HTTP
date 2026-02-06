from common.http_session import create_session

BASE_URL = "https://httpbin.org"

def run():
    session = create_session()

    response = session.get(
        f"{BASE_URL}/redirect-to?url=/get",
        allow_redirects=True
    )

    print("Final URL:", response.url)
    print("Response:", response.json())

if __name__ == "__main__":
    run()
