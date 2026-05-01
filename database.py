from auth import hash_password

user_db = {
    "admin@example.com": {
        "id": 1,
        "email": "admin@example.com",
        "hashed_password": hash_password("password123")
    }
}

session_db = {}
