import allure
import requests

from constants import ORDERS_URL, REQUEST_TIMEOUT


@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Авторизованный пользователь создаёт заказ с ингредиентом")
    def test_authorized_user_can_create_order(self, user_factory, ingredient_id):
        user = user_factory()

        response = requests.post(
            ORDERS_URL,
            json={"ingredients": [ingredient_id]},
            headers={"Authorization": user["token"]},
            timeout=REQUEST_TIMEOUT,
        )

        assert response.status_code == 200, response.text
        body = response.json()
        assert body["success"] is True
        assert body["order"]["number"] > 0
        assert body["name"]

    @allure.title("Создание заказа без авторизации запрещено")
    def test_unauthorized_user_cannot_create_order(self, ingredient_id):
        response = requests.post(
            ORDERS_URL, json={"ingredients": [ingredient_id]}, timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }

    @allure.title("Заказ без ингредиентов отклоняется")
    def test_order_without_ingredients_is_rejected(self, user_factory):
        user = user_factory()
        response = requests.post(
            ORDERS_URL,
            json={"ingredients": []},
            headers={"Authorization": user["token"]},
            timeout=REQUEST_TIMEOUT,
        )

        assert response.status_code == 400
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided",
        }

    @allure.title("Неверный хеш ингредиента приводит к ошибке сервера")
    def test_order_with_invalid_ingredient_hash_is_rejected(self, user_factory):
        user = user_factory()
        response = requests.post(
            ORDERS_URL,
            json={"ingredients": ["invalid_ingredient_hash"]},
            headers={"Authorization": user["token"]},
            timeout=REQUEST_TIMEOUT,
        )

        assert response.status_code == 500
        assert response.text
