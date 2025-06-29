"""Database operations

Database and all crud operations
"""

from datetime import datetime

from sqlalchemy import (
    create_engine,
    Connection,
    TypeAdapter,
    desc,
    insert,
    update,
    select,
)

from app.core.config import settings
from app.core.base_model import MessageBatch, User, UserCreate, UserUpdate, Message
from app.core.secret import get_passwd_hash
from app.core.base_model_db import user_db, message_db, chat_db


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)


# TODO: transfer all database request into async
def create_user_db(conn: Connection, user_create: UserCreate) -> User:
    user_create_data = user_create.model_dump()

    user_secure = User(
        **user_create_data, hashed_passwd=get_passwd_hash(user_create.passwd)
    )

    conn.execute(insert(user_db), [user_secure.model_dump(mode="json")])
    return user_secure


def update_user_db(conn: Connection, user_update: UserUpdate) -> User | None:
    update_data = user_update.model_dump(exclude_defaults=True, mode="json")
    updated_users = conn.execute(
        update(user_db)
        .where(user_db.c.login == update_data["login"])
        .returning(user_db),
        [update_data],
    )
    if updated_users.rowcount != 1:
        raise ValueError("Cant update user, wrong data")
    # .first() may return None and ._mapping dont work with None
    user_dict = dict(updated_users.first()._mapping)  # type: ignore
    return User(**user_dict)


def get_user_db(conn: Connection, user_name: str) -> User | None:
    user = conn.execute(select(user_db).where(user_db.c.login == user_name))
    if user.rowcount == 0:
        return None
    elif user.rowcount == 1:
        # .first() may return None and ._mapping dont work with None
        return User(dict(user.first()._mapping))  # type: ignore
    else:
        raise ValueError("Get >2 users with same login")


# TODO: add crate group function, some day:)
# def create_group(conn: Connection, group_name: str, user_logins: list[str]):
#     pass


def store_message_db(conn: Connection, message: Message) -> Message:
    conn.execute(insert(message_db), [message.model_dump(mode="json")])
    return message


def get_message_batch_db(
    conn: Connection,
    chat_name: str,
    last_message_time: datetime | None = None,
    msg_count: int = 200,
) -> MessageBatch | None:
    chat_id_subq = select(chat_db.c.id).where(chat_db.c.name == chat_name).subquery()
    msg_batch_query = (
        select(message_db)
        .where(message_db.c.user_id == chat_id_subq)
        .where(message_db.c.send_at <= last_message_time)
        .order_by(desc(message_db.c.send_at))
        .limit(msg_count)
    )

    msg_batch = conn.execute(msg_batch_query)

    batch_size = msg_batch.rowcount
    if batch_size == 0:
        return None
    # Dump batch
    msg_adapter = TypeAdapter(list[Message])
    msg_arr = msg_adapter.validate_python([dict(msg._mapping) for msg in msg_batch])
    first_message_time = msg_arr[0]["send_at"]
    last_message_time = msg_arr[-1]["send_at"]
    return MessageBatch(
        message_arr=msg_arr,
        batch_size=batch_size,
        first_message_time=first_message_time,
        last_message_time=last_message_time,
    )


# def get_last_message(conn: Connection, chat_name: str) -> Message:
#     pass

# def get_chat_user_list(conn: Connection, chat_name: str):
#     pass
