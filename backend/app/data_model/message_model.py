from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated


from app.core.config import settings


class MessageCreate(BaseModel):
    chat_id: int
    user_id: int
    message_text: str


class Message(MessageCreate):
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
    message_arr: list[Message]
    last_message_time: datetime
    first_message_time: datetime
