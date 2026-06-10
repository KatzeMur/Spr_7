import requests
import allure
from constants import BASE_URL, COURIER_ENDPOINT, COURIER_LOGIN_ENDPOINT
from utils import generate_random_string, generate_courier_payload

class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_successfully(self, courier_login):
        with allure.step("Генерация тестовых данных"):
            payload = generate_courier_payload()
            payload["login"] = courier_login
        
        with allure.step("Отправка POST-запроса на создание курьера"):
            response = requests.post(f'{BASE_URL}{COURIER_ENDPOINT}', data=payload)
        
        with allure.step("Проверка кода ответа и тела ответа"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    @allure.title("Создание курьера с уже существующим логином")
    def test_create_duplicate_courier(self, registered_courier):
        with allure.step("Повторная попытка регистрации с данными из фикстуры"):
            response = requests.post(f'{BASE_URL}{COURIER_ENDPOINT}', data=registered_courier)
        
        with allure.step("Проверка кода ответа 409 (Конфликт)"):
            assert response.status_code == 409

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        with allure.step("Формирование payload без поля login"):
            payload = {
                "password": generate_random_string(10),
                "firstName": generate_random_string(10)
            }
            
        with allure.step("Отправка POST-запроса"):
            response = requests.post(f'{BASE_URL}{COURIER_ENDPOINT}', data=payload)
            
        with allure.step("Проверка кода ответа 400 (Bad Request)"):
            assert response.status_code == 400

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        with allure.step("Формирование payload без поля password"):
            payload = {
                "login": generate_random_string(10),
                "firstName": generate_random_string(10)
            }
            
        with allure.step("Отправка POST-запроса"):
            response = requests.post(f'{BASE_URL}{COURIER_ENDPOINT}', data=payload)
            
        with allure.step("Проверка кода ответа 400 (Bad Request)"):
            assert response.status_code == 400


class TestLoginCourier:
    @allure.title("Успешный логин курьера")
    def test_login_courier_successfully(self, registered_courier):
        with allure.step("Отправка POST-запроса на логин с данными из фикстуры"):
            login_payload = {
                "login": registered_courier["login"],
                "password": registered_courier["password"]
            }
            response = requests.post(f'{BASE_URL}{COURIER_LOGIN_ENDPOINT}', data=login_payload)
        
        with allure.step("Проверка кода ответа и наличия id в теле ответа"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Логин курьера без логина")
    def test_login_courier_without_login(self):
        with allure.step("Формирование payload без поля login"):
            payload = {
                "password": generate_random_string(10)
            }
            
        with allure.step("Отправка POST-запроса на логин"):
            response = requests.post(f'{BASE_URL}{COURIER_LOGIN_ENDPOINT}', data=payload)
            
        with allure.step("Проверка кода ответа 400 (Bad Request)"):
            assert response.status_code == 400

    @allure.title("Логин несуществующего курьера")
    def test_login_non_existent_courier(self):
        with allure.step("Генерация случайных данных для несуществующего пользователя"):
            payload = {
                "login": generate_random_string(10),
                "password": generate_random_string(10)
            }
            
        with allure.step("Отправка POST-запроса на логин"):
            response = requests.post(f'{BASE_URL}{COURIER_LOGIN_ENDPOINT}', data=payload)
            
        with allure.step("Проверка кода ответа 404 (Not Found)"):
            assert response.status_code == 404

    @allure.title("Логин курьера с пустым паролем")
    def test_login_courier_without_password(self):
        with allure.step("Формирование payload с пустым паролем"):
            payload = {
                "login": generate_random_string(10),
                "password": ""
            }
            
        with allure.step("Отправка POST-запроса на логин"):
            response = requests.post(f'{BASE_URL}{COURIER_LOGIN_ENDPOINT}', json=payload)
            
        with allure.step("Проверка кода ответа 400 (Bad Request)"):
            assert response.status_code == 400
            