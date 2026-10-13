from uuid import uuid4


def generate_user_data():
    suffix = uuid4().hex
    return {
        "email": f"api_test_{suffix}@example.com",
        "password": f"Password_{suffix}",
        "name": f"Test User {suffix[:8]}",
    }
