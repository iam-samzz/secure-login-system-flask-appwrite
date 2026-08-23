from argon2 import PasswordHasher



ph = PasswordHasher()

#generates hash password
def generate_password_hash(password: str) -> dict:
    try:
        hashed_password = ph.hash(password)

        return {
            "success": True,
            "message": "Password hashed successfully",
            "password": hashed_password
        }

    except TypeError:
        return {
            "success": False,
            "error": "invalid password",
            "message": "Password must be a valid text string"
        }

    except Exception:
        return {
            "success": False,
            "error": "Internal server error"
        }

