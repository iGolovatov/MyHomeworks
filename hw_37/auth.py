USERS = [
    {
        "username": "admin",
        "api_key": "admin_secret_key_123",
        "role": "admin"
    },
    {
        "username": "user",
        "api_key": "user_readonly_key_456",
        "role": "user"
    }
]


def is_valid_api_key(api_key):
    return any(user["api_key"] == api_key for user in USERS)


def is_admin(api_key):
    return any(user["api_key"] == api_key and user["role"] == "admin" for user in USERS)
