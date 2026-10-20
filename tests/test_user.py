import allure
import pytest

from data import INVALID_CREDENTIALS, UNAUTHORIZED


@allure.feature("Изменение данных пользователя")
class TestUser:
    @pytest.mark.parametrize("field", ["email", "name"])
    @allure.title("Авторизованный пользователь меняет поле {field}")
    def test_authorized_user_can_update_profile_field(
        self, api_client, registered_user, field
    ):
        new_value = f"updated_{registered_user['data'][field]}"
        response = api_client.update_user(
            {field: new_value}, registered_user["token"]
        )

        assert response.status_code == 200, response.text
        registered_user["data"][field] = new_value
        expected_body = {
            "success": True,
            "user": {
                "email": registered_user["data"]["email"],
                "name": registered_user["data"]["name"],
            },
        }
        assert response.json() == expected_body

        profile_response = api_client.get_user(registered_user["token"])
        assert profile_response.status_code == 200, profile_response.text
        assert profile_response.json() == expected_body

    @allure.title("Авторизованный пользователь меняет пароль")
    def test_authorized_user_can_update_password(self, api_client, registered_user):
        new_password = f"updated_{registered_user['data']['password']}"
        response = api_client.update_user(
            {"password": new_password}, registered_user["token"]
        )

        assert response.status_code == 200, response.text
        registered_user["data"]["password"] = new_password
        assert response.json() == {
            "success": True,
            "user": {
                "email": registered_user["data"]["email"],
                "name": registered_user["data"]["name"],
            },
        }
        login_response = api_client.login_user(
            {
                "email": registered_user["data"]["email"],
                "password": new_password,
            }
        )
        assert login_response.status_code == 200
        assert login_response.json()["user"] == {
            "email": registered_user["data"]["email"],
            "name": registered_user["data"]["name"],
        }

    @pytest.mark.parametrize("field", ["email", "name"])
    @allure.title("Изменение поля {field} без авторизации запрещено")
    def test_unauthorized_user_cannot_update_profile_field(
        self, api_client, registered_user, field
    ):
        response = api_client.update_user(
            {field: f"updated_{registered_user['data'][field]}"}
        )

        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED
        profile_response = api_client.get_user(registered_user["token"])
        assert profile_response.status_code == 200
        assert profile_response.json() == {
            "success": True,
            "user": {
                "email": registered_user["data"]["email"],
                "name": registered_user["data"]["name"],
            },
        }

    @allure.title("Изменение пароля без авторизации запрещено")
    def test_unauthorized_user_cannot_update_password(
        self, api_client, registered_user
    ):
        new_password = f"updated_{registered_user['data']['password']}"
        response = api_client.update_user({"password": new_password})

        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED
        old_credentials = {
            "email": registered_user["data"]["email"],
            "password": registered_user["data"]["password"],
        }
        old_login = api_client.login_user(old_credentials)
        assert old_login.status_code == 200
        assert old_login.json()["user"] == {
            "email": registered_user["data"]["email"],
            "name": registered_user["data"]["name"],
        }
        new_login = api_client.login_user(
            {"email": registered_user["data"]["email"], "password": new_password}
        )
        assert new_login.status_code == 401
        assert new_login.json() == INVALID_CREDENTIALS
