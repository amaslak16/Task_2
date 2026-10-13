import os


BASE_URL = os.getenv("STELLAR_BURGERS_URL", "https://stellarburgers.education-services.ru")
REGISTER_URL = f"{BASE_URL}/api/auth/register"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
USER_URL = f"{BASE_URL}/api/auth/user"
INGREDIENTS_URL = f"{BASE_URL}/api/ingredients"
ORDERS_URL = f"{BASE_URL}/api/orders"
REQUEST_TIMEOUT = 15
