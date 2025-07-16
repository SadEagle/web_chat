from enum import IntEnum
from sqlalchemy import Column, ForeignKey, MetaData, Table, UniqueConstraint, func
from sqlalchemy.types import Integer, String, Text, DateTime


metadata_obj = MetaData()

# TODO: transform all datetime into triggers those write those values
user_db = Table(
    "user_info",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("login", String(255), unique=True),
    Column("email", String(255), unique=True),
    Column("hashed_passwd", String(255)),
    Column("create_at", DateTime, server_default=func.now()),
)

# TODO: add indexation across send_at, maybe also add something to user_id
message_db = Table(
    "message",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("message_text", Text),
    Column("send_at", DateTime, server_default=func.now(), index=True),
    Column("chat_id", ForeignKey("chat.id")),
    Column("user_info_id", ForeignKey("user_info.id")),
    # TODO: fix this partition feture if possible
    # Postgre specific split table on subtables, search across one of them
    # postgresql_partition_by="range(chat_id)",
)

chat_db = Table(
    "chat",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), unique=True),
)

chat_user_db = Table(
    "group_user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_info_id", ForeignKey("user_info.id")),
    Column("chat_id", ForeignKey("chat.id")),
    UniqueConstraint("user_info_id", "chat_id", name="chat_user_unique"),
)
