import requests
import random

s = random.randint(10000,999999)
BASE_URL = "http://localhost:8000"
EMAIL = f"test_api_user{str(s)}@example.com"
PASSWORD = "123456"

def get_token():
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": EMAIL, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get("access_token")
    assert token, "No token returned"
    return token


def test_register():
    response = requests.post(
        f"{BASE_URL}/register",
        data={"username": EMAIL, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code in (200, 400)


def test_login_and_get_token():
    token = get_token()
    assert isinstance(token, str)
    assert len(token) > 10


def test_prediction_endpoints():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # /prediction
    r1 = requests.get(f"{BASE_URL}/prediction", headers=headers)
    assert r1.status_code == 200
    assert "prediction" in r1.json()

    # /prediction/history
    r2 = requests.get(f"{BASE_URL}/prediction/history", headers=headers)
    assert r2.status_code == 200
    assert "history" in r2.json()