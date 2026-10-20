import allure
import pytest

from data import INVALID_CREDENTIALS


@allure.feature("Авторизация пользователя")
class TestLogin:
    @allure.title("Зарегистрированный пользователь может войти")
    def test_login_with_valid_credentials(self, api_client, registered_user):
        credentials = {
            key: registered_user["data"][key] for key in ("email", "password")
        }
        response = api_client.login_user(credentials)

        body = response.json()
        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {
            "email": registered_user["data"]["email"],
            "name": registered_user["data"]["name"],
        }
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @pytest.mark.parametrize("invalid_field", ["email", "password"])
    @allure.title("Вход с неверным полем {invalid_field} запрещён")
    def test_login_with_invalid_credentials(self, api_client, registered_user, invalid_field):
        credentials = {
            key: registered_user["data"][key] for key in ("email", "password")
        }
        credentials[invalid_field] = f"wrong_{credentials[invalid_field]}"

        response = api_client.login_user(credentials)

        assert response.status_code == 401
        assert response.json() == INVALID_CREDENTIALS
