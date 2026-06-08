import pytest
import requests
from constants import BASE_URL

class TestCreateOrder:
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": "Тестин",
            "lastName": "Тестинов",
            "address": "Улица Тестовая, дом 1",
            "metroStation": 1,
            "phone": "+79991234567",
            "rentTime": 1,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ",
            "color": color
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()

class TestGetOrdersList:
    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        
        assert response.status_code == 200
        assert "orders" in response.json()
        