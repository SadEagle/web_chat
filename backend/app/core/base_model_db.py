from enum import IntEnum
from sqlalchemy import Column, ForeignKey, MetaData, Table, func
from sqlalchemy.types import Integer, String, Text, Date, DateTime


metadata_obj = MetaData()

user_db = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("login", String(50), unique=True),
    Column("email", String(50), unique=True),
    Column("hashed_passwd", String(50), unique=True),
    Column("create_at", Date, default=func.current_date()),
    Column("last_activity_at", DateTime, default=func.current_timestamp()),
)

# TODO: add indexing by creation date
message_db = Table(
    "message",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("message_text", Text),
    Column("send_at", Integer),
    Column("chat_id", ForeignKey("chat.id")),
    Column("user_id", ForeignKey("user.id")),
)

chat_db = Table(
    "chat",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), unique=True),
)

chat_user_db = Table(
    "group_user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id")),
    Column("chat_id", ForeignKey("chat.id")),
)
