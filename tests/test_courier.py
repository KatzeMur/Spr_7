import requests
import random
import string
from constants import BASE_URL

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_create_courier_successfully():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    response = requests.post(
        f'{BASE_URL}/api/v1/courier', 
        data=payload
    )
    
    assert response.status_code == 201
    assert response.json() == {"ok": True}

def test_create_duplicate_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    
    assert response.status_code == 409

def test_create_courier_without_login():
    payload = {
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    assert response.status_code == 400

def test_create_courier_without_password():
    payload = {
        "login": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    assert response.status_code == 400

def test_login_courier_successfully():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    create_payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    requests.post(f'{BASE_URL}/api/v1/courier', data=create_payload)
    
    login_payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=login_payload)
    
    assert response.status_code == 200
    assert "id" in response.json()

def test_login_courier_without_login():
    payload = {
        "password": generate_random_string(10)
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    assert response.status_code == 400

def test_login_non_existent_courier():
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10)
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    assert response.status_code == 404

def test_login_courier_without_password():
    payload = {
        "login": generate_random_string(10),
        "password": ""
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', json=payload)
    assert response.status_code == 400
    