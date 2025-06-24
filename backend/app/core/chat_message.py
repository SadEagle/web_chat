from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Sending message info"""

    group_name: str
    user: str
    message_text: str
