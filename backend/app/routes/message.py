from fastapi import APIRouter, HTTPException, status

from app.deps import ConnectionDep, UserTokenExtractDep
from app.data_model.message_model import (
    MessageCreate,
    MessageBatch,
    MessageBatchRequest,
)
from app.data_model.token_model import TokenData
from app.crud_model.message_crud import get_message_batch_db, store_message_db


message_route_prefix = "/message"
message_route = APIRouter(prefix=message_route_prefix)


@message_route.post("/send_message", status_code=status.HTTP_204_NO_CONTENT)
def send_message(
    conn: ConnectionDep,
    user_token: UserTokenExtractDep,
    msg: MessageCreate,
):
    if user_token.user_id != msg.user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Token user differ from login user, somehow",
        )
    store_message_db(conn, msg)
    # TODO: Add sending message by websocket for all active users for their chats updates
    return None


@message_route.put("/get_batch_message")
def get_batch_message(
    conn: ConnectionDep,
    user_token: UserTokenExtractDep,
    message_batch_request: MessageBatchRequest,
) -> MessageBatch | None:
    # TODO: add security check that user is inside current group
    message_batch = get_message_batch_db(
        conn,
        message_batch_request.chat_id,
        message_batch_request.last_message_time,
        message_batch_request.batch_size,
    )

    return message_batch
