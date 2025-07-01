from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.deps import ConnectionDep
from app.crud import create_user_db, get_user_db
from app.secret import create_access_token, verify_access_token, verify_passwd_hash
from app.core.base_model import Token, UserCreate, UserToken, UserDB
from app.core.config import settings
from app.exceptions import DuplicateError


login_route_prefix = "/login"
login_route = APIRouter(prefix=login_route_prefix)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=login_route_prefix + "/login_user")


def get_user_by_token(token: Annotated[str, Depends(oauth2_scheme)]) -> UserToken:
    user_token = verify_access_token(token)
    if user_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authentificate": "Bearer"},
        )
    return user_token


# TODO: add update
# @login_route.post("/update_data")
# def login_user(
#     conn: ConnectionDep,
#     user_update: UserUpdate,
# ) -> UserOut:
#     pass


# TODO: add connection_manager (websocket)
# TODO: add redirection to main page!? if token already exists
@login_route.post("/login_user")
def generate_user_token(
    conn: ConnectionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = get_user_db(conn, form_data.username)
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User wasn't found")

    if not verify_passwd_hash(form_data.password, user.hashed_passwd):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Wrong login or password")

    access_token = create_access_token(
        # UserToken(login=form_data.username),
        UserToken(id=user.id),
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@login_route.post("/create_user", status_code=status.HTTP_201_CREATED)
def registry_user(conn: ConnectionDep, user_create: UserCreate) -> UserDB:
    try:
        user_created = create_user_db(conn, user_create)
    except DuplicateError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))
    return user_created
