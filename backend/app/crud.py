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
    ChatDB,
    ChatUserCreate,
    ChatUserDB,
    UserDB,
    UserCreateSecure,
    UserUpdateSecure,
    MessageCreate,
    MessageDB,
    MessageBatch,
)
from app.core.base_db_model import user_db, message_db, chat_user_db, chat_db
from app.deps import ConnectionDep
from app.exceptions import DuplicateError


msg_adapter = TypeAdapter(list[MessageDB])
chat_user_list_adapter = TypeAdapter(list[UserDB])
chat_user_per_line_adapter = TypeAdapter(list[ChatUserDB])


def create_user_db(conn: ConnectionDep, user_secure: UserCreateSecure) -> UserDB | None:
    try:
        user_result = conn.execute(
            insert(user_db)
            .returning(user_db)
            .values(user_secure.model_dump(mode="json"))
        ).mappings()
    except IntegrityError as exc:
        if "UNIQUE constraint failed: user.login" in str(exc):
            raise DuplicateError(f"Login '{user_secure.login}' already exists")
        elif "UNIQUE constraint failed: user.email" in str(exc):
            raise DuplicateError(f"Email '{user_secure.email}' already exists")
        else:
            raise DuplicateError(f"Unexpected duplicate value. {exc}")
    # TODO: fix
    user_row = user_result.first()
    if user_row is None:
        return None
    return UserDB.model_validate(user_row)


def update_user_db(
    conn: ConnectionDep, user_secret_update: UserUpdateSecure
) -> UserDB | None:
    try:
        updated_users = conn.execute(
            update(user_db)
            .where(user_db.c.id == user_secret_update.user_id)
            .returning(user_db)
            .values(
                user_secret_update.model_dump(
                    exclude_defaults=True,
                    mode="json",
                    by_alias=True,
                )
            )
        ).mappings()
    except IntegrityError as exc:
        if "email" in str(exc).lower():
            raise DuplicateError(f"Email '{user_secret_update.email}' already exists")
        else:
            raise DuplicateError("Unexpected column duplicate")
    user_row = updated_users.first()
    if user_row is None:
        return None
    return UserDB.model_validate(user_row)


def get_user_db(conn: ConnectionDep, user_name: str) -> UserDB | None:
    user = conn.execute(select(user_db).where(user_db.c.login == user_name))
    user_row = user.first()
    if user_row is None:
        return None
    return UserDB.model_validate(user_row._mapping)


# TODO: check
def get_chat_user_list(conn: ConnectionDep, chat_id: int) -> list[UserDB]:
    user_list = conn.execute(
        select(chat_user_db).where(chat_user_db.c.chat_id == chat_id)
    ).mappings()
    return chat_user_list_adapter.validate_python(user_list)


# TODO: check
def create_chat(conn: ConnectionDep, chat_name: str) -> ChatDB:
    try:
        created_chat = conn.execute(
            insert(chat_db).returning(chat_db).values(name=chat_name)
        ).mappings()
    except IntegrityError as exc:
        if "UNIQUE constraint failed: chat.name" in str(exc):
            raise DuplicateError(f"Chat name '{chat_name}' already exists")
        else:
            raise DuplicateError("Unexpected column duplicate")
    return ChatDB.model_validate(created_chat.first())


def create_chat_user_list(
    conn: ConnectionDep, chat_user_create: ChatUserCreate
) -> list[ChatUserDB]:
    try:
        chat_user_updated = conn.execute(
            insert(chat_user_db),
            list(
                map(
                    lambda user_id: {
                        "chat_id": chat_user_create.chat_id,
                        "user_id": user_id,
                    },
                    chat_user_create.user_id_list,
                )
            ),
        ).mappings()
    # TODO: Change error to log and ignore 2nd adding certain user?
    except IntegrityError:
        raise DuplicateError("Some users already added")
    return chat_user_per_line_adapter.validate_python(chat_user_updated)


def store_message_db(conn: ConnectionDep, message: MessageCreate) -> MessageDB | None:
    message_data = message.model_dump(mode="json")
    message_result = conn.execute(
        insert(message_db).returning(message_db).values(message_data)
    )
    message_row = message_result.first()
    if message_row is None:
        return None
    return MessageDB.model_validate(message_row._mapping)


# TODO: think that this search script not that efficent on huge texts. Probably, need to make some marks what date is above
def get_message_batch_db(
    conn: ConnectionDep,
    chat_id: int,
    last_message_time: datetime | None = None,
    msg_count: int = 200,
) -> MessageBatch | None:
    if last_message_time is None:
        msg_batch_query = (
            select(message_db)
            .where(message_db.c.user_id == chat_id)
            .order_by(desc(message_db.c.send_at))
            .limit(msg_count)
        )
    else:
        msg_batch_query = (
            select(message_db)
            .where(message_db.c.chat_id == chat_id)
            .where(message_db.c.send_at <= last_message_time)
            .order_by(desc(message_db.c.send_at))
            .limit(msg_count)
        )
    msg_batch_seq = conn.execute(msg_batch_query).mappings().fetchall()
    if len(msg_batch_seq) == 0:
        return None
    msg_arr = msg_adapter.validate_python([msg for msg in msg_batch_seq])
    first_message_time = msg_arr[0].send_at
    last_message_time = msg_arr[-1].send_at
    return MessageBatch(
        chat_id=chat_id,
        message_arr=msg_arr,
        batch_size=msg_count,
        first_message_time=first_message_time,
        last_message_time=last_message_time,
    )


# def get_chat_user_list(conn: Connection, chat_name: str) -> :
#     pass
