from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.deps import ConnectionDep
from app.core.db import create_user_db, get_user_db
from app.core.secret import create_access_token, verify_access_token
from app.core.base_model import Token, UserCreate, UserToken, User
from app.core.config import settings


login_route = APIRouter(prefix="login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token_bearer")


def get_user_per_login(token: Annotated[str, oauth2_scheme]) -> UserToken:
    user_token = verify_access_token(token)
    if user_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authentificate": "Bearer"},
        )
    return user_token


@login_route.post("/token")
def generate_user_token(
    conn: ConnectionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token | None:
    try:
        user = get_user_db(conn, form_data.username)
    except ValueError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Current login has duplicates in database, somehow",
        )
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong login")

    access_token = create_access_token(
        UserToken(login=form_data.username),
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@login_route.post("/create_user")
async def registry_user(conn: ConnectionDep, user_create: UserCreate) -> User:
    return create_user_db(conn, user_create)
