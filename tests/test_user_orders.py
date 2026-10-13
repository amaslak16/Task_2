import allure
import requests

from constants import ORDERS_URL, REQUEST_TIMEOUT


@allure.feature("Заказы пользователя")
class TestUserOrders:
    @allure.title("Авторизованный пользователь получает свои заказы")
    def test_authorized_user_can_get_own_orders(self, user_factory, ingredient_id):
        user = user_factory()
        headers = {"Authorization": user["token"]}
        created_order = requests.post(
            ORDERS_URL,
            json={"ingredients": [ingredient_id]},
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        assert created_order.status_code == 200, created_order.text
        order_number = created_order.json()["order"]["number"]

        response = requests.get(ORDERS_URL, headers=headers, timeout=REQUEST_TIMEOUT)

        assert response.status_code == 200, response.text
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["orders"], list)
        assert any(order["number"] == order_number for order in body["orders"])
        assert isinstance(body["total"], int)
        assert isinstance(body["totalToday"], int)

    @allure.title("Без авторизации заказы пользователя недоступны")
    def test_unauthorized_user_cannot_get_orders(self):
        response = requests.get(ORDERS_URL, timeout=REQUEST_TIMEOUT)

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }
