import os
from requests.auth import HTTPBasicAuth
from common.http_session import create_session

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; if not installed, fall back to environment variables
    pass

BASE_URL = os.getenv("INGESTION_BASE_URL", "https://httpbin.org")
USERNAME = os.getenv("INGESTION_BASIC_USER")
PASSWORD = os.getenv("INGESTION_BASIC_PASS")

def run():
    if not USERNAME or not PASSWORD:
        print("ERROR: Las variables de entorno INGESTION_BASIC_USER / INGESTION_BASIC_PASS no están definidas.\n" \
              "Crea un archivo .env (no subir a Git) o exporta las variables antes de ejecutar.")
        return

    session = create_session()

    response = session.get(
        f"{BASE_URL}/basic-auth/{USERNAME}/{PASSWORD}",
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    print("Status code:", response.status_code)
    try:
        data = response.json()
        # Mostrar solo el estado de autenticación y ocultar el usuario
        if isinstance(data, dict) and 'authenticated' in data:
            print("Response:", {"authenticated": data.get('authenticated')})
        else:
            # Si la respuesta no tiene la clave esperada, imprimir la respuesta completa
            print("Response:", data)
    except Exception:
        print("Response text:", response.text)


if __name__ == "__main__":
    run()
