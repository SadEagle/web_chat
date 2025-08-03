from enum import StrEnum

import secrets
from pydantic_settings import BaseSettings


class RunMode(StrEnum):
    PROD = "prod"
    DEV = "dev"
    TEST = "test"


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_HASH_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    # TODO: add some day token for token
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    FRONTEND_HOST: str = "http://localhost:5573"

    PROJECT_NAME: str = "TeleChat"
    BATCH_MESSAGE_SIZE: int = 50
    RUN_MODE: RunMode = RunMode.DEV
    # TODO: isolate in late future
    # SQLALCHEMY_PROD_DB_URL: str = (
    #     "postgresql://chatter:secret@postgres-db:5432/prod_chat"
    #
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DEV_DB_URL: str = "postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@postgres-db:5432/{self.POSTGRES_DB}"
    # SQLALCHEMY_TEST_DB_URL: str = "postgresql://chatter:secret@postgres-db:5432/test_chat"
    # SQLALCHEMY_PROD_DB_URL: str = "sqlite:///test_chat.db"
    SQLALCHEMY_DEV_DB_URL: str = "sqlite:///test_chat.db"
    SQLALCHEMY_TEST_DB_URL: str = "sqlite:///test_chat.db"


settings = Settings()
