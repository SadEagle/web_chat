"""Singleton connection manager."""

from asyncio import gather
from operator import itemgetter

from fastapi import WebSocket

from app.core.chat_message import ChatMessage


class ConnectionManager:
    """Active user websockets managment"""

    # Special prefix for personal chats
    PERSONAL_CHAT_PREFIX: str = "__prefix__"

    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_name: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_name] = websocket

    def disconnect(self, user_name: str) -> None:
        self.active_connections.pop(user_name)

    @classmethod
    def get_users_from_personal_chat(cls, group_name: str) -> tuple[str, str]:
        """Get both users from personal chat name"""
        group_prefix, *user_names = group_name.split("_")
        if not group_name.startswith(cls.PERSONAL_CHAT_PREFIX) or len(user_names) != 2:
            err_msg = "Unexpected chat name. Expected personal chat"
            raise ValueError(err_msg)
        return user_names[0], user_names[1]

    async def send_personal_message(
        self, message: ChatMessage, websocket: WebSocket
    ) -> None:
        """Optimised 2 user messaging

        Optimised message send via personal chat storage both user names inside itself
        """
        await websocket.send_text(message.message_text)

    async def send_group_message(self, user_list: list[str], message: str) -> None:
        socket_getter = itemgetter(*user_list)
        users_broadcast = [
            connection.send_text(message)
            for connection in socket_getter(self.active_connections)
        ]
        # It doesnt matter if some users cant send message
        # TODO: add error websocket validation
        await gather(*users_broadcast)


connection_manager = ConnectionManager()
