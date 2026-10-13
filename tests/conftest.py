import pytest

from api_client import ApiClient
from helpers import generate_user_data


@pytest.fixture
def api_client():
    return ApiClient()


@pytest.fixture
def user_factory(api_client):
    created_users = []

    def create_user():
        data = generate_user_data()
        response = api_client.register_user(data)
        token = response.json().get("accessToken") if response.status_code == 200 else None
        user = {"data": data, "response": response, "token": token}
        if token:
            created_users.append(user)
        return user

    yield create_user

    for user in created_users:
        response = api_client.delete_user(user["token"])
        if response.status_code == 401:
            credentials = {key: user["data"][key] for key in ("email", "password")}
            login_response = api_client.login_user(credentials)
            if login_response.status_code != 200:
                raise RuntimeError(f"Не удалось войти для удаления: {login_response.text}")
            response = api_client.delete_user(login_response.json()["accessToken"])
        if response.status_code not in (200, 202) or response.json().get("success") is not True:
            raise RuntimeError(f"Не удалось удалить тестового пользователя: {response.text}")


@pytest.fixture
def registered_user(user_factory):
    user = user_factory()
    if user["response"].status_code != 200 or not user["token"]:
        raise RuntimeError(f"Не удалось создать тестового пользователя: {user['response'].text}")
    return user


@pytest.fixture
def ingredient_id(api_client):
    response = api_client.get_ingredients()
    if response.status_code != 200:
        raise RuntimeError(f"Не удалось получить ингредиенты: {response.text}")
    ingredients = response.json()["data"]
    if not ingredients:
        raise RuntimeError("API вернул пустой список ингредиентов")
    return ingredients[0]["_id"]


@pytest.fixture
def user_with_order(api_client, registered_user, ingredient_id):
    response = api_client.create_order([ingredient_id], registered_user["token"])
    if response.status_code != 200:
        raise RuntimeError(f"Не удалось создать тестовый заказ: {response.text}")
    return registered_user, response.json()["order"]["number"]
