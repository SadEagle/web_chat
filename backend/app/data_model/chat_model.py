from typing import Annotated, TypeAlias
from pydantic import BaseModel, Field, TypeAdapter


ChatName: TypeAlias = Annotated[str, Field(max_length=255)]

ChatListAdapter = TypeAdapter(list["Chat"])


class ChatCreate(BaseModel):
    name: ChatName
    user_id_list: list[int]


class ChatUpdate(BaseModel):
    """Add several users or exclude yourself. If chat empty - delete chat"""

    name: ChatName | None = None
    user_id_include: list[int] | None = None
    self_exclude: bool | None


class ChatDelete(BaseModel):
    id: int


# TODO: make function that will return
class Chat(BaseModel):
    """Minimal chat info db"""

    id: int
    name: ChatName
    user_id_list: list[int]
