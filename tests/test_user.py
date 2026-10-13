import allure
import pytest
import requests

from constants import LOGIN_URL, REQUEST_TIMEOUT, USER_URL


@allure.feature("Изменение данных пользователя")
class TestUser:
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Авторизованный пользователь меняет поле {field}")
    def test_authorized_user_can_update_any_field(self, user_factory, field):
        user = user_factory()
        old_data = user["data"].copy()
        new_value = f"updated_{old_data[field]}"

        response = requests.patch(
            USER_URL,
            json={field: new_value},
            headers={"Authorization": user["token"]},
            timeout=REQUEST_TIMEOUT,
        )

        assert response.status_code == 200, response.text
        user["data"][field] = new_value
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {
            "email": user["data"]["email"],
            "name": user["data"]["name"],
        }
        if field == "password":
            login_response = requests.post(
                LOGIN_URL,
                json={"email": old_data["email"], "password": new_value},
                timeout=REQUEST_TIMEOUT,
            )
            assert login_response.status_code == 200, login_response.text
            assert login_response.json()["success"] is True

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Изменение поля {field} без авторизации запрещено")
    def test_unauthorized_user_cannot_update_any_field(self, user_factory, field):
        user = user_factory()
        original_data = user["data"].copy()

        response = requests.patch(
            USER_URL,
            json={field: f"updated_{original_data[field]}"},
            timeout=REQUEST_TIMEOUT,
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }
        profile_response = requests.get(
            USER_URL,
            headers={"Authorization": user["token"]},
            timeout=REQUEST_TIMEOUT,
        )
        assert profile_response.status_code == 200
        assert profile_response.json()["user"] == {
            "email": original_data["email"],
            "name": original_data["name"],
        }
        if field == "password":
            login_response = requests.post(
                LOGIN_URL,
                json={
                    "email": original_data["email"],
                    "password": original_data["password"],
                },
                timeout=REQUEST_TIMEOUT,
            )
            assert login_response.status_code == 200
            assert login_response.json()["success"] is True
