from datetime import datetime

from sqlalchemy.exc import IntegrityError  # OperationalError
from pydantic import TypeAdapter
from sqlalchemy import (
    desc,
    insert,
    update,
    select,
)

from app.core.base_model import (
    UserSecret,
    BaseUser,
    UserDB,
    UserCreate,
    UserSecretCreate,
    UserUpdate,
    MessageDB,
    MessageCreate,
)
from app.secret import get_passwd_hash
from app.core.base_model_db import user_db, message_db, chat_db
from app.deps import ConnectionDep
from app.exceptions import DuplicateError


# TODO: transfer all database request into async
def create_user_db(conn: ConnectionDep, user_create: UserCreate) -> UserDB:
    user_create_data = user_create.model_dump()

    user_secure = UserSecretCreate(
        **user_create_data, hashed_passwd=get_passwd_hash(user_create.passwd)
    )
    try:
        user_result = conn.execute(
            insert(user_db)
            .returning(user_db)
            .values(user_secure.model_dump(mode="json"))
        )
    except IntegrityError as exc:
        if "UNIQUE constraint failed: user.login" in str(exc):
            raise DuplicateError(f"Login '{user_secure.login}' already exists")
        elif "UNIQUE constraint failed: user.email" in str(exc):
            raise DuplicateError(f"Email '{user_secure.email}' already exists")
        else:
            raise DuplicateError(f"Unexpected duplicate value")
    return UserDB(**user_result.first()._mapping)  # type: ignore


def update_user_db(conn: ConnectionDep, user_update: UserUpdate) -> BaseUser:
    update_data = user_update.model_dump(exclude_defaults=True, mode="json")
    try:
        updated_users = conn.execute(
            update(user_db)
            .where(user_db.c.login == update_data["login"])
            .returning(user_db)
            .values(update_data)
        )
    except IntegrityError as exc:
        if "email" in str(exc).lower():
            raise DuplicateError(f"Email '{user_update.email}' already exists")
        else:
            raise DuplicateError(f"Unexpected column duplicate")
    user_dict = dict(updated_users.first()._mapping)  # type: ignore
    return BaseUser(**user_dict)


def get_user_db(conn: ConnectionDep, user_name: str) -> UserSecret | None:
    user = conn.execute(select(user_db).where(user_db.c.login == user_name)).mappings()
    user_data = user.fetchall()
    if len(user_data) == 0:
        return None
    return UserSecret(**user_data[0])


# TODO: add crate group function, some day:)
# def create_group(conn: Connection, group_name: str, user_logins: list[str]):
#     pass


def store_message_db(conn: ConnectionDep, message: MessageCreate) -> MessageDB:
    message_data = message.model_dump(mode="json")
    message_result = conn.execute(
        insert(message_db).returning(message_db).values(message_data)
    )
    return MessageDB(**message_result.first()._mapping)


# def get_message_batch_db(
#     conn: ConnectionDep,
#     chat_name: str,
#     last_message_time: datetime | None = None,
#     msg_count: int = 200,
# ) -> MessageBatch | None:
#     chat_id_subq = select(chat_db.c.id).where(chat_db.c.name == chat_name).subquery()
#     if last_message_time is None:
#         msg_batch_query = (
#             select(message_db)
#             .where(message_db.c.user_id == chat_id_subq)
#             .order_by(desc(message_db.c.send_at))
#             .limit(msg_count)
#         )
#     else:
#         msg_batch_query = (
#             select(message_db)
#             .where(message_db.c.user_id == chat_id_subq)
#             .where(message_db.c.send_at <= last_message_time)
#             .order_by(desc(message_db.c.send_at))
#             .limit(msg_count)
#         )
#
#     msg_batch = conn.execute(msg_batch_query)
#
#     batch_size = msg_batch.rowcount
#     if batch_size == 0:
#         return None
#     msg_adapter = TypeAdapter(list[Message])
#     msg_arr = msg_adapter.validate_python([dict(msg._mapping) for msg in msg_batch])
#     first_message_time = msg_arr[0].send_at
#     last_message_time = msg_arr[-1].send_at
#     return MessageBatch(
#         message_arr=msg_arr,
#         batch_size=batch_size,
#         first_message_time=first_message_time,
#         last_message_time=last_message_time,
#     )


# def get_last_message(conn: Connection, chat_name: str) -> Message:
#     pass

# def get_chat_user_list(conn: Connection, chat_name: str):
#     pass
