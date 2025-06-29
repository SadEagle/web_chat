from fastapi import APIRouter

from app.core.base_model import Message, MessageBatchRequest
from app.deps import ConnectionDep
from backend.app.core.db import store_message_db


message_route = APIRouter(prefix="/message")


@message_route.post("/send_message")
async def send_message(conn: ConnectionDep, msg: Message):
    # TODO: Use combination websocket for notification and user verification
    store_message_db(conn, msg)


async def get_batch_message(
    conn: ConnectionDep, message_batch_request: MessageBatchRequest
):
    pass
