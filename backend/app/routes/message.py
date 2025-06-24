from fastapi import APIRouter
from pydantic import BaseModel


message_route = APIRouter()


@message_route.post("send_message")
def send_message(msg: ChatMessage):
    # TODO:
    # 0. Get user_list from valkey server
    # 1. Send message to sqlalchemy
    # 2. Check existence of the chat and send confirmation to user that message was ok (may be add icon for message like telegram)
    # 3. Create task queue send messages to clients. Probably simple option to make one more process
    pass
