import allure

from data import UNAUTHORIZED


@allure.feature("Заказы пользователя")
class TestUserOrders:
    @allure.title("Авторизованный пользователь получает свои заказы")
    def test_authorized_user_can_get_own_orders(self, api_client, user_with_order):
        user, order_number = user_with_order
        response = api_client.get_user_orders(user["token"])

        assert response.status_code == 200, response.text
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["orders"], list)
        assert [order["number"] for order in body["orders"]] == [order_number]
        assert isinstance(body["total"], int)
        assert isinstance(body["totalToday"], int)

    @allure.title("Без авторизации заказы пользователя недоступны")
    def test_unauthorized_user_cannot_get_orders(self, api_client):
        response = api_client.get_user_orders()

        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED
