import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_HASH_ALGORITHM: str = "HS256"
    # WARN: Dummy value
    JDBC_ENGINE = "sqlite://"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    # TODO: add some day token for token
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    FRONTEND_HOST: str = "http://localhost:5573"

    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URL: str = "sqlite:///:memory:"


settings = Settings()  # type: ignore
