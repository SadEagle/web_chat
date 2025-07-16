import pytest
from typing import Generator, cast

from fastapi.testclient import TestClient

from app.main import app
from app.core.db import engine
from app.data_model.db_model import metadata_obj
from app.core.secret import create_access_token

from app.data_model.user_model import UserCreate
from app.data_model.token_model import TokenData
from app.crud_model.user_crud import create_user_db
from app.deps import ConnectionDep
from tests.utils import random_email, random_login, random_lower_string, UserTokenTest


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
def user_token_test() -> UserTokenTest:
    user_test = UserCreate(
        login=random_login(),
        email=random_email(),
        passwd=random_lower_string(),
    )

    with engine.begin() as conn:
        user_out = create_user_db(conn, user_test)
    if user_out is None:
        raise RuntimeError("Cant create test user")
    token_data = TokenData(user_id=user_out.id)

    token = create_access_token(token_data)
    return UserTokenTest(
        id=user_out.id,
        login=user_test.login,
        email=user_test.email,
        passwd=user_test.passwd,
        token=token,
    )


# TODO:
# 1. add chat group
# 2. add 3 messages for this chat group
# 3. add test user for this test_group
