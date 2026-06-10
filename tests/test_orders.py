import pytest
import requests
import allure
from constants import BASE_URL, ORDERS_ENDPOINT
from data.orders_data import ORDER_PAYLOAD_TEMPLATE

class TestCreateOrder:
    @allure.title("Создание заказа с различными комбинациями цветов")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        with allure.step("Формирование payload заказа с добавлением цвета"):
            payload = ORDER_PAYLOAD_TEMPLATE.copy()
            payload["color"] = color
        
        with allure.step("Отправка POST-запроса на создание заказа"):
            response = requests.post(f'{BASE_URL}{ORDERS_ENDPOINT}', json=payload)
        
        with allure.step("Проверка кода ответа и наличия track в теле ответа"):
            assert response.status_code == 201
            assert "track" in response.json()

class TestGetOrdersList:
    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        with allure.step("Отправка GET-запроса на получение списка заказов"):
            response = requests.get(f'{BASE_URL}{ORDERS_ENDPOINT}')
        
        with allure.step("Проверка кода ответа и наличия orders в теле ответа"):
            assert response.status_code == 200
            assert "orders" in response.json()
            