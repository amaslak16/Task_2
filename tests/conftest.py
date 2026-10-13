import pytest
import requests

from constants import INGREDIENTS_URL, LOGIN_URL, REGISTER_URL, REQUEST_TIMEOUT, USER_URL
from helpers import generate_user_data


@pytest.fixture
def user_factory():
    created_users = []

    def create_user():
        data = generate_user_data()
        response = requests.post(REGISTER_URL, json=data, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 200, response.text
        token = response.json()["accessToken"]
        user = {"data": data, "response": response, "token": token}
        created_users.append(user)
        return user

    yield create_user

    for user in created_users:
        token = user["token"]
        response = requests.delete(
            USER_URL, headers={"Authorization": token}, timeout=REQUEST_TIMEOUT
        )
        if response.status_code == 401:
            login_response = requests.post(
                LOGIN_URL,
                json={key: user["data"][key] for key in ("email", "password")},
                timeout=REQUEST_TIMEOUT,
            )
            assert login_response.status_code == 200, login_response.text
            response = requests.delete(
                USER_URL,
                headers={"Authorization": login_response.json()["accessToken"]},
                timeout=REQUEST_TIMEOUT,
            )
        assert response.status_code in (200, 202), response.text
        assert response.json()["success"] is True


@pytest.fixture
def ingredient_id():
    response = requests.get(INGREDIENTS_URL, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text
    ingredients = response.json()["data"]
    assert ingredients, "API returned an empty ingredient list"
    return ingredients[0]["_id"]
