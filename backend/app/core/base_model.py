from datetime import datetime
from typing import Annotated, TypeAlias

from pydantic import BaseModel, EmailStr, Field, BeforeValidator

from app.core.config import settings
from app.core.secret import get_passwd_hash


UserLogin: TypeAlias = Annotated[str, Field(max_length=255)]
UserEmail: TypeAlias = Annotated[EmailStr, Field(max_length=255)]
UserHashedPasswd: TypeAlias = Annotated[
    str, Field(validation_alias="passwd"), BeforeValidator(get_passwd_hash)
]


class UserBaseCreate(BaseModel):
    login: UserLogin
    email: UserEmail


class UserCreate(UserBaseCreate):
    passwd: Annotated[str, Field(max_length=50)]


class UserCreateSecure(UserBaseCreate):
    """Transformation UserCreate in secure form

    Attributes:
        hashed_passwd: hashed password
    """

    hashed_passwd: UserHashedPasswd


class UserDB(UserBaseCreate):
    """User representation from database user_db

    Attributes:
        hashed_passwd: hashed password
        user_id: user id, alias for id column (user_db.c.id)
        create_at: user creation time in db
    """

    hashed_passwd: str
    user_id: Annotated[int, Field(alias="id")]
    create_at: datetime


class UserDBOut(BaseModel):
    """Return to client dataclass, mostly for UserDB filter

    Attributes:
        user_id: user id column (user_id.c.id)
    """

    user_id: int
    login: UserLogin


class UserBaseUpdate(BaseModel):
    """Update User Model. All fields update are optional

    Attributes:
        user_id: user id with serrialization alias (user_db.c.id)
        login: login
        email: email
    """

    # Database store as id param
    user_id: Annotated[int, Field(serialization_alias="id")]
    login: UserLogin | None = None
    email: UserEmail | None = None


class UserUpdate(UserBaseUpdate):
    passwd: str | None = Field(max_length=50, default=None)


class UserUpdateSecure(UserBaseUpdate):
    hashed_passwd: UserHashedPasswd | None = None


class MessageCreate(BaseModel):
    chat_id: int
    user_id: int
    message_text: str


class MessageDB(MessageCreate):
    send_at: datetime


class MessageBatchRequest(BaseModel):
    # WARN: make it proper with other id -> user_id transformations
    user_id: int
    chat_id: int
    batch_size: int = settings.BATCH_MESSAGE_SIZE
    last_message_time: Annotated[datetime, Field(default_factory=datetime.now)]


class MessageBatch(BaseModel):
    chat_id: int
    batch_size: int
    message_arr: list[MessageDB]
    last_message_time: datetime
    first_message_time: datetime


class ChatDB(BaseModel):
    chat_id: Annotated[int, Field(alias="id")]
    name: Annotated[str, Field(max_length=50)]


class ChatUserCreate(BaseModel):
    chat_id: int
    user_id_list: list[int]


class ChatUserDB(BaseModel):
    chat_id: int
    user_id: int
