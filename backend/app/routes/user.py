from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.deps import ConnectionDep, UserTokenExtractDep
from app.crud_model.user_crud import create_user_db, get_user_db, update_user_db
from app.core.secret import (
    create_access_token,
    verify_passwd_hash,
)
from app.data_model.user_model import (
    UserCreate,
    UserUpdate,
    UserOut,
)
from app.data_model.token_model import TokenData, TokenCreate
from app.core.config import settings
from app.exceptions import DuplicateError, NoCreatedElementError


user_route_prefix = "/user"
user_route = APIRouter(prefix=user_route_prefix)


@user_route.post("/update_user")
def update_user(
    conn: ConnectionDep,
    user_token: UserTokenExtractDep,
    user_update: UserUpdate,
) -> UserOut:
    if user_update.id != user_token.user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Token user differ from update user, somehow",
        )
    try:
        updated_user = update_user_db(conn, user_update)
    except DuplicateError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))

    if updated_user is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Cant find user for update",
        )
    return UserOut.model_validate(updated_user.model_dump(mode="json"))


@user_route.post("/login_user")
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
        TokenData(user_id=user.id),
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenCreate(access_token=access_token, token_type="bearer")


@user_route.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(conn: ConnectionDep, user_create: UserCreate) -> UserOut:
    try:
        user_created = create_user_db(conn, user_create)
    except DuplicateError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))
    if user_created is None:
        raise NoCreatedElementError("User wasn't created")
    return UserOut.model_validate(user_created.model_dump(mode="json"))
