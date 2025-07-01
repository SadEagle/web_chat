import jwt
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext

from app.core.base_model import UserToken
from app.core.config import settings


crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_passwd_hash(passwd: str) -> str:
    return crypto_context.hash(passwd, scheme="bcrypt")


def verify_passwd_hash(passwd: str, hash_passwd: str) -> bool:
    """Verify password with hashed db password

    Args:
        passwd: password
        hash_passwd: password hash

    Returns:
        True, if passwd and hash_passwd are equal, False otherwise
    """
    return crypto_context.verify(passwd, hash_passwd)


def create_access_token(
    data: UserToken,
    expires_delta: timedelta = timedelta(minutes=15),
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    encode_data = {
        **data.model_dump(),
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        encode_data, settings.SECRET_KEY, algorithm=settings.JWT_HASH_ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str) -> UserToken | None:
    try:
        user_data = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.JWT_HASH_ALGORITHM
        )
    except jwt.ExpiredSignatureError:
        return None
    return UserToken(**user_data)
