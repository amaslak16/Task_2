import allure
import pytest

from data import REQUIRED_REGISTRATION_FIELDS, USER_ALREADY_EXISTS
from helpers import generate_user_data


@allure.feature("Регистрация пользователя")
class TestRegistration:
    @allure.title("Уникальный пользователь успешно регистрируется")
    def test_register_unique_user(self, user_factory):
        user = user_factory()
        response = user["response"]
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {
            "email": user["data"]["email"],
            "name": user["data"]["name"],
        }
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Повторная регистрация существующего пользователя запрещена")
    def test_register_existing_user(self, api_client, registered_user):
        response = api_client.register_user(registered_user["data"])

        assert response.status_code == 403
        assert response.json() == USER_ALREADY_EXISTS

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Регистрация без обязательного поля {missing_field} запрещена")
    def test_register_without_required_field(self, api_client, missing_field):
        data = generate_user_data()
        data.pop(missing_field)

        response = api_client.register_user(data)

        assert response.status_code == 403
        assert response.json() == REQUIRED_REGISTRATION_FIELDS
