import allure
import requests

from constants import (
    INGREDIENTS_URL,
    LOGIN_URL,
    ORDERS_URL,
    REGISTER_URL,
    REQUEST_TIMEOUT,
    USER_URL,
)


class ApiClient:
    @allure.step("Зарегистрировать пользователя")
    def register_user(self, data):
        return requests.post(REGISTER_URL, json=data, timeout=REQUEST_TIMEOUT)

    @allure.step("Авторизовать пользователя")
    def login_user(self, credentials):
        return requests.post(LOGIN_URL, json=credentials, timeout=REQUEST_TIMEOUT)

    @allure.step("Получить данные пользователя")
    def get_user(self, token):
        return requests.get(
            USER_URL, headers={"Authorization": token}, timeout=REQUEST_TIMEOUT
        )

    @allure.step("Изменить данные пользователя")
    def update_user(self, data, token=None):
        headers = {"Authorization": token} if token else None
        return requests.patch(
            USER_URL, json=data, headers=headers, timeout=REQUEST_TIMEOUT
        )

    @allure.step("Удалить пользователя")
    def delete_user(self, token):
        return requests.delete(
            USER_URL, headers={"Authorization": token}, timeout=REQUEST_TIMEOUT
        )

    @allure.step("Получить ингредиенты")
    def get_ingredients(self):
        return requests.get(INGREDIENTS_URL, timeout=REQUEST_TIMEOUT)

    @allure.step("Создать заказ")
    def create_order(self, ingredients, token=None):
        headers = {"Authorization": token} if token else None
        return requests.post(
            ORDERS_URL,
            json={"ingredients": ingredients},
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    @allure.step("Получить заказы пользователя")
    def get_user_orders(self, token=None):
        headers = {"Authorization": token} if token else None
        return requests.get(ORDERS_URL, headers=headers, timeout=REQUEST_TIMEOUT)
