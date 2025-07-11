import pytest
from typing import Generator, cast

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.main import app
from app.core.db import engine, metadata_obj
from app.core.secret import create_access_token

from app.core.base_model import UserCreate, UserCreateSecure
from app.core.base_token_model import TokenData
from app.crud import create_user_db
from app.deps import ConnectionDep
from tests.utils import random_email, random_login, random_lower_string, TestUserToken


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    return TestClient(app)


# DB operations unit tests fixture
@pytest.fixture
def db_operations() -> Generator[ConnectionDep, None, None]:
    with engine.begin() as conn:
        yield cast(ConnectionDep, conn)


@pytest.fixture(scope="session", autouse=True)
def db_clear():
    yield
    metadata_obj.drop_all(engine)


@pytest.fixture(scope="module")
def user_token_test() -> TestUserToken:
    test_user = UserCreate(
        login=random_login(),
        email=random_email(),
        passwd=random_lower_string(),
    )
    test_user_secure = UserCreateSecure.model_validate(
        test_user.model_dump(mode="json")
    )

    with engine.begin() as conn:
        user_out = create_user_db(conn, test_user_secure)
    if user_out is None:
        raise RuntimeError("Cant create test user")
    token_data = TokenData(user_id=user_out.user_id)

    token = create_access_token(token_data)
    return TestUserToken(
        user_id=user_out.user_id,
        login=test_user.login,
        email=test_user.email,
        passwd=test_user.passwd,
        token=token,
    )
