from dataclasses import dataclass
import random
import string

from pydantic import BaseModel

from app.core.base_model import UserCreate, UserUpdate


class TestUserToken(BaseModel):
    user_id: int
    login: str
    email: str
    passwd: str
    token: str


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_login() -> str:
    return random_lower_string()


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_create_user() -> UserCreate:
    return UserCreate(
        login=random_login(),
        email=random_email(),
        passwd=random_lower_string(),
    )


def get_update_user(user_id: int) -> UserUpdate:
    return UserUpdate(
        user_id=user_id,
        login=random_login(),
        email=random_email(),
        passwd=random_lower_string(),
    )
