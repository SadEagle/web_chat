from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


login_route = APIRouter(prefix="/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@login_route.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO: add user verification with inner sqlalchemy database if not exist then
    # create (dont manage special key for login)
    return {"access_token": "dummy_token", "token_type": "bearer"}


# TODO: Add create user option
# @login_route.put("/create_user")
# def create_user()


# TODO: Add change password option
