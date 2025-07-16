from fastapi import APIRouter, HTTPException, status

from app.deps import ConnectionDep, UserTokenExtractDep
from app.data_model.chat_model import ChatCreate, Chat, ChatUpdate
from app.crud_model.chat_crud import create_chat_db
from app.exceptions import DuplicateError


chat_route_prefix = "/chat"
chat_route = APIRouter(prefix=chat_route_prefix)


# TODO: !!!!! Need to check that all users are exists
# But... in this case wont it will be better to return data about them at the same time?
@chat_route.post("/create_chat", status_code=status.HTTP_201_CREATED)
def create_chat(
    conn: ConnectionDep, user_token: UserTokenExtractDep, chat_create: ChatCreate
) -> Chat:
    try:
        chat = create_chat_db(conn, chat_create, user_token)
    except DuplicateError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))
    return chat


# @chat_route.post(chat_route_prefix + "/update_chat")
# def update_chat(conn: ConnectionDep, user_token: UserTokenExtractDep, chat_update: ChatUpdate) -> Chat:
#     try
#

# TODO: add verification that it's possible
# def delete_user_chat()
