from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, status

from app.deps import ConnectionDep, UserTokenExtractDep
from app.data_model.chat_model import ChatCreate, Chat
from app.crud_model.chat_crud import (
    create_chat_db,
    get_chats_data_db,
    get_current_user_chat_ids_db,
)
from app.exceptions import DuplicateError


chat_route_prefix = "/chat"
chat_route = APIRouter(prefix=chat_route_prefix)


@chat_route.post("/create_chat", status_code=status.HTTP_201_CREATED)
def create_chat(
    conn: ConnectionDep, user_token: UserTokenExtractDep, chat_create: ChatCreate
) -> Chat:
    try:
        created_chat = create_chat_db(conn, chat_create, user_token)
    except DuplicateError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    return created_chat


@chat_route.put("/get_current_user_chat_ids", tags=["Init"])
def get_current_user_chats_by_token(
    conn: ConnectionDep, user_token: UserTokenExtractDep
) -> list[int]:
    """Get chat ids for current user by it's token"""
    return get_current_user_chat_ids_db(conn, user_token.user_id)


@chat_route.put("/get_full_chats_data")
def get_full_chats_data(
    conn: ConnectionDep,
    user_token: UserTokenExtractDep,
    chat_ids: Annotated[list[int], Body],
) -> list[Chat]:
    """Get chats data by it's ids"""
    return get_chats_data_db(conn, chat_ids)


# @chat_route.patch(chat_route_prefix + "/update_chat")
# def update_chat(conn: ConnectionDep, user_token: UserTokenExtractDep, chat_update: ChatUpdate) -> Chat:
#     try
#

# TODO: add verification that it's possible
# @chat_route.delete(....)
# def delete_user_chat()
