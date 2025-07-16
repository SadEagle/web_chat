from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Connection

from app.core.db import engine
from app.data_model.token_model import TokenData
from app.core.secret import verify_access_token


def get_db() -> Generator[Connection, None, None]:
    with engine.begin() as conn:
        yield conn


ConnectionDep = Annotated[Connection, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login_user")


def extract_token_data(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    user_token = verify_access_token(token)
    if user_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authentificate": "Bearer"},
        )
    return user_token


UserTokenExtractDep = Annotated[TokenData, Depends(extract_token_data)]
