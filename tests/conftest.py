import pytest
import requests
from constants import BASE_URL, COURIER_ENDPOINT
from utils import generate_random_string, generate_courier_payload

@pytest.fixture
def courier_login():
    login = generate_random_string(10)
    yield login
    requests.delete(f'{BASE_URL}{COURIER_ENDPOINT}', json={"login": login})

@pytest.fixture
def registered_courier():
    payload = generate_courier_payload()
    requests.post(f'{BASE_URL}{COURIER_ENDPOINT}', data=payload)
    yield payload
    requests.delete(f'{BASE_URL}{COURIER_ENDPOINT}', json={"login": payload["login"]})
    