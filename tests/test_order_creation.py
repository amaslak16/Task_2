import allure

from data import INGREDIENTS_REQUIRED, UNAUTHORIZED


@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Авторизованный пользователь создаёт заказ с ингредиентом")
    def test_authorized_user_can_create_order(
        self, api_client, registered_user, ingredient_id
    ):
        response = api_client.create_order(
            [ingredient_id], registered_user["token"]
        )

        assert response.status_code == 200, response.text
        body = response.json()
        assert body["success"] is True
        assert body["order"]["number"] > 0
        assert body["name"]

    @allure.title("Создание заказа без авторизации запрещено")
    def test_unauthorized_user_cannot_create_order(self, api_client, ingredient_id):
        response = api_client.create_order([ingredient_id])

        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED

    @allure.title("Заказ без ингредиентов отклоняется")
    def test_order_without_ingredients_is_rejected(self, api_client, registered_user):
        response = api_client.create_order([], registered_user["token"])

        assert response.status_code == 400
        assert response.json() == INGREDIENTS_REQUIRED

    @allure.title("Неверный хеш ингредиента приводит к ошибке сервера")
    def test_order_with_invalid_ingredient_hash_is_rejected(
        self, api_client, registered_user
    ):
        response = api_client.create_order(
            ["invalid_ingredient_hash"], registered_user["token"]
        )

        assert response.status_code == 500
        assert response.reason == "Internal Server Error"
