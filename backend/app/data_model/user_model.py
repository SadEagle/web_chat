from datetime import datetime
from typing import Annotated, TypeAlias

from pydantic import BaseModel, EmailStr, Field, TypeAdapter

from app.data_model.chat_model import Chat

UserLogin: TypeAlias = Annotated[str, Field(max_length=255)]
UserEmail: TypeAlias = Annotated[EmailStr, Field(max_length=255)]
UserPasswd: TypeAlias = Annotated[str, Field(max_length=255)]

UserListAdapter = TypeAdapter(list["User"])
UserOutListAdapter = TypeAdapter(list["UserOut"])


class UserBaseCreate(BaseModel):
    login: UserLogin
    email: UserEmail


class UserCreate(UserBaseCreate):
    """User creation data

    Attributes:
        passwd: password
    """

    passwd: UserPasswd


class UserCreateSecure(UserBaseCreate):
    """Pre-db storage data representation

    Attributes:
        id: user id
        hashed_passwd: hashed password
    """

    hashed_passwd: str


class UserUpdateBase(BaseModel):
    id: int
    login: UserLogin | None = None
    email: UserEmail | None = None


class UserUpdate(UserUpdateBase):
    passwd: UserPasswd | None = None


class UserUpdateSecure(UserUpdateBase):
    hashed_passwd: str | None = None


class User(UserCreateSecure):
    """User representation from database user_db

    Attributes:
        hashed_passwd: hashed password
        user_id: user id, alias for id column (user_db.c.id)
        create_at: user creation time in db
    """

    id: int
    create_at: datetime


class UserOut(BaseModel):
    """Data returning from API

    Attributes:
        user_id: user id column (user_id.c.id)
    """

    user_id: Annotated[int, Field(validation_alias="id")]
    login: UserLogin


class UserChatList(BaseModel):
    """Chat list per user"""

    user_id: int
    chat_list: list[Chat]
