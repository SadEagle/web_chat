from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.deps import ConnectionDep
from app.crud import create_user_db, get_user_db, update_user_db
from app.core.secret import (
    create_access_token,
    verify_access_token,
    verify_passwd_hash,
)
from app.core.base_model import (
    UserCreate,
    UserDBOut,
    UserCreateSecure,
    UserUpdateSecure,
    UserUpdate,
)
from app.core.base_token_model import TokenData, TokenCreate
from app.core.config import settings
from app.exceptions import DuplicateError, NoCreatedElementError


login_route_prefix = "/login"
login_route = APIRouter(prefix=login_route_prefix)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=login_route_prefix + "/login_user")


def get_user_by_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    user_token = verify_access_token(token)
    if user_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authentificate": "Bearer"},
        )
    return user_token


@login_route.post("/update_user")
def login_user(
    conn: ConnectionDep,
    user_update: UserUpdate,
    user_token: Annotated[TokenData, Depends(get_user_by_token)],
) -> UserDBOut:
    if user_update.user_id != user_token.user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Token user differ from update user, somehow",
        )
    # if user_update.passwd is not None:
    #     user_update_secret = UserUpdateSecure(
    #         **user_update.model_dump(mode="json"),
    #         hashed_passwd=get_passwd_hash(user_update.passwd),
    #     )
    # else:
    #     user_update_secret = UserUpdateSecure.model_validate(user_update)
    user_update_secret = UserUpdateSecure.model_validate(
        user_update.model_dump(mode="json")
    )
    try:
        updated_user = update_user_db(conn, user_update_secret)
    except DuplicateError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))

    if updated_user is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Cant find user for update",
        )
    return UserDBOut.model_validate(updated_user.model_dump(mode="json"))


@login_route.post("/login_user")
def generate_user_token(
    conn: ConnectionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenCreate:
    user = get_user_db(conn, form_data.username)
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User wasn't found")

    if not verify_passwd_hash(form_data.password, user.hashed_passwd):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Wrong login or password")

    access_token = create_access_token(
        # UserToken(login=form_data.username),
        TokenData(user_id=user.user_id),
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenCreate(access_token=access_token, token_type="bearer")


@login_route.post("/create_user", status_code=status.HTTP_201_CREATED)
def registry_user(conn: ConnectionDep, user_create: UserCreate) -> UserDBOut:
    # user_secure = UserCreateSecure(
    #     **user_create_data, hashed_passwd=get_passwd_hash(user_create.passwd)
    # )
    user_secure = UserCreateSecure.model_validate(user_create.model_dump(mode="json"))
    try:
        user_created = create_user_db(conn, user_secure)
    except DuplicateError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))
    if user_created is None:
        raise NoCreatedElementError("User wasn't created")
    return UserDBOut.model_validate(user_created.model_dump(mode="json"))
