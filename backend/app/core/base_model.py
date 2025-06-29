from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class UserToken(BaseModel):
    login: str = Field(max_length=50)


class BaseUser(UserToken):
    email: EmailStr = Field(max_length=50)


class UserCreate(BaseUser):
    passwd: str = Field(max_length=50)


class UserOut(BaseUser):
    create_time: date
    last_activity_time: datetime
    create_at: int
    last_activity_at: int


class User(UserOut):
    hashed_passwd: str


class UserUpdate(BaseModel):
    login: str = Field(max_length=50)
    email: EmailStr | None = Field(max_length=50, default=None)
    hashed_passwd: str | None = Field(max_length=50, default=None)


class Message(BaseModel):
    group_name: str
    user_name: str
    message_text: str
    send_at: int


class MessageBatchRequest(BaseModel):
    batch_size: int
    last_message_time: datetime | None = None


class MessageBatch(MessageBatchRequest):
    message_arr: list[Message]
    first_message_time: datetime | None = None
