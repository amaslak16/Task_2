import allure
import pytest
import requests

from constants import REGISTER_URL, REQUEST_TIMEOUT
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
    def test_register_existing_user(self, user_factory):
        user = user_factory()

        response = requests.post(
            REGISTER_URL, json=user["data"], timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": "User already exists"}

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Регистрация без обязательного поля {missing_field} запрещена")
    def test_register_without_required_field(self, missing_field):
        data = generate_user_data()
        data.pop(missing_field)

        response = requests.post(REGISTER_URL, json=data, timeout=REQUEST_TIMEOUT)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields",
        }
