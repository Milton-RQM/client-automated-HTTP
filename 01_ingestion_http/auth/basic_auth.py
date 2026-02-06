from requests.auth import HTTPBasicAuth
from common.http_session import create_session

BASE_URL = "https://httpbin.org"

def run():
    session = create_session()

    response = session.get(
        f"{BASE_URL}/basic-auth/usuario_test/clave123",
        auth=HTTPBasicAuth("usuario_test", "clave123")
    )

    print("Status code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    run()
