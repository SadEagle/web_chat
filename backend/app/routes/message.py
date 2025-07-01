from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core.core_schema import model_ser_schema

from app.deps import ConnectionDep
from app.core.base_model import UserToken, MessageCreate
from app.crud import store_message_db
from app.routes.login import get_user_by_token
from app.core.connection_manager import connection_manager


message_route = APIRouter(prefix="/message")


# TODO: add connection_manager (websocket)
@message_route.post("/send_message", status_code=status.HTTP_204_NO_CONTENT)
def send_message(
    conn: ConnectionDep,
    user_token: Annotated[UserToken, Depends(get_user_by_token)],
    msg: MessageCreate,
):
    if user_token.id != msg.user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Token user differ from login user, somehow",
        )
    store_message_db(conn, msg)
    # TODO: Add sending message by websocket for all active users for their chats updates
    return None


# # TODO: some complex stuff with valkeydb for next batch and for faster message getting?!
# # Not sure how should it work with multiple users?
# # I mean, it may be good just to store last batch for every group?
# @message_route.post("/get_batch_message")
# def get_batch_message(
#     conn: ConnectionDep,
#     user_token: Annotated[UserToken, Depends(get_user_by_token)],
#     message_batch_request: MessageBatchRequest,
# ):
#     pass
