from faker import Faker
from common.http_session import create_session

fake = Faker()
BASE_URL = "https://httpbin.org"

def run():
    session = create_session()

    payload = {
        "name": fake.name(),
        "email": fake.email(),
        "message": fake.sentence()
    }

    response = session.post(f"{BASE_URL}/post", data=payload)
    print(response.json())

if __name__ == "__main__":
    run()
