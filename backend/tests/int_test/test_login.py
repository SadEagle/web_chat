from app.core.base_model import UserUpdate
from tests.utils import TestUserToken, get_create_user, get_update_user


def test_create_user(test_app):
    user = get_create_user()

    response = test_app.post("/login/create_user", json=user.model_dump(mode="json"))
    assert response.status_code == 201
    assert response.json()["login"] == user.login


def test_create_duplicate_user(test_app):
    user_data = get_create_user().model_dump(mode="json")

    response_create = test_app.post("/login/create_user", json=user_data)
    response_duplicate = test_app.post("/login/create_user", json=user_data)
    assert response_create.status_code == 201 and response_duplicate.status_code == 400
    assert response_create.json()["login"] == response_create.json()["login"]


# NOTE: test only full update and not partial
def test_update_user(test_app, user_token_test: TestUserToken):
    """Update test user and update back"""
    user_test_default = UserUpdate.model_validate(
        user_token_test.model_dump(mode="json")
    ).model_dump(mode="json")
    user_update_test = get_update_user(user_id=user_token_test.user_id).model_dump(
        mode="json"
    )
    bearer_header = {"Authorization": f"Bearer {user_token_test.token}"}
    response = test_app.post(
        "/login/update_user",
        json=user_update_test,
        headers=bearer_header,
    )
    response_data = response.json()
    assert user_update_test["user_id"] == response_data["user_id"]
    assert user_update_test["login"] == response_data["login"]

    # Request return back default test user
    response_default = test_app.post(
        "/login/update_user",
        json=user_test_default,
        headers=bearer_header,
    )
    response_data_default = response_default.json()
    assert user_token_test.user_id == response_data_default["user_id"]
    assert user_token_test.login == response_data_default["login"]


def test_login_user(test_app, user_token_test):
    """Try to login test user"""
    result = test_app.post(
        "/login/login_user",
        data={"username": user_token_test.login, "password": user_token_test.passwd},
    )
    result_data = result.json()
    assert result.status_code == 200
    assert result_data["token_type"] == "bearer"
    assert "access_token" in result_data


def test_login_user_wrong(test_app, user_token_test):
    """Try to login test user wrong"""
    result = test_app.post(
        "/login/login_user",
        data={
            "username": user_token_test.login,
            "password": user_token_test.passwd + "AKJSDLKASJLADQ",
        },
    )
    assert result.status_code == 400
