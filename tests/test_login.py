import allure
import pytest
import requests

from constants import LOGIN_URL, REQUEST_TIMEOUT


@allure.feature("Авторизация пользователя")
class TestLogin:
    @allure.title("Зарегистрированный пользователь может войти")
    def test_login_with_valid_credentials(self, user_factory):
        user = user_factory()

        response = requests.post(
            LOGIN_URL,
            json={key: user["data"][key] for key in ("email", "password")},
            timeout=REQUEST_TIMEOUT,
        )

        body = response.json()
        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {
            "email": user["data"]["email"],
            "name": user["data"]["name"],
        }
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @pytest.mark.parametrize("invalid_field", ["email", "password"])
    @allure.title("Вход с неверным полем {invalid_field} запрещён")
    def test_login_with_invalid_credentials(self, user_factory, invalid_field):
        user = user_factory()
        credentials = {key: user["data"][key] for key in ("email", "password")}
        credentials[invalid_field] = f"wrong_{credentials[invalid_field]}"

        response = requests.post(LOGIN_URL, json=credentials, timeout=REQUEST_TIMEOUT)

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect",
        }
