from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    validate_password_strength(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str):
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters long.")

    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number.")

    if not re.search(r"[!@#$%^&*(),.?" "':{}|<>]", password):
        raise ValueError("Password must contain at least one special character.")

    weak_passwords = ["password123", "admin123", "welcome123", "reconx123"]
    if password.lower() in weak_passwords:
        raise ValueError("Password is too weak.")
