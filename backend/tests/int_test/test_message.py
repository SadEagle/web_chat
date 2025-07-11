# import pytest
# from fastapi.testclient import TestClient
#
# from backend.app.exceptions import DuplicateError
# from tests.utils import random_email, random_login, random_lower_string
# from app.main import app
# from app.core.base_model import UserCreate
#
#
# test_client = TestClient(app)
#
#
# @pytest.fixture
# def create_user():
#     return UserCreate(
#         login=random_login(),
#         email=random_email(),
#         passwd=random_lower_string(),
#     )
#     # token = test_client.post(
#     #     "/login/create_user", json=user_create.model_dump(mode="json")
#     # )
#     #
#     # @pytest.fixture
#     # def user_setup(self):
#     #     pass
#     #
#     # def test_send_message(self):
#     #     pass
