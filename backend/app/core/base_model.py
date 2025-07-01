from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class UserToken(BaseModel):
    # User_id
    id: int


class BaseUser(UserToken):
    login: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)


class UserCreate(BaseUser):
    passwd: str = Field(max_length=50)


class UserSecretCreate(BaseUser):
    hashed_passwd: str


class UserDB(BaseUser):
    id: int
    create_at: datetime


class UserSecret(UserDB):
    hashed_passwd: str


# TODO: sended message may be different
class UserUpdate(BaseModel):
    login: str = Field(max_length=50)
    email: EmailStr | None = Field(max_length=50, default=None)
    hashed_passwd: str | None = Field(max_length=50, default=None)


class MessageCreate(BaseModel):
    chat_id: int
    user_id: int
    message_text: str


class MessageDB(MessageCreate):
    send_at: datetime


# class MessageBatchRequest(BaseModel):
#     batch_size: int
#     last_message_time: datetime | None = None
#
#
# class MessageBatch(MessageBatchRequest):
#     message_arr: list[Message]
#     first_message_time: datetime | None = None
