from sqlalchemy import delete, exists, insert, select, func, text
from sqlalchemy.exc import IntegrityError

from app.exceptions import DuplicateError
from app.deps import ConnectionDep
from app.data_model.db_model import chat_user_db, chat_db
from app.data_model.chat_model import ChatCreate, Chat, ChatUpdate, ChatDelete
from app.data_model.token_model import TokenData


def delete_chat_db(conn: ConnectionDep, chat_delete: ChatDelete) -> ChatDelete:
    return ChatDelete.model_validate(
        conn.execute(delete(chat_db).where(chat_db.c.id == chat_delete.id))
        .mappings()
        .first()
    )


def get_minimal_chat_db(conn: ConnectionDep, chat_id: int) -> Chat | None:
    chat_user_list_arr = (
        conn.execute(
            select(
                # TODO: check with attention aggregation function, does it really return list?
                func.array_agg(chat_user_db.c.user_info_id).alias("user_id_list")
            ).where(chat_user_db.c.chat_id == chat_id)
        )
        .mappings()
        .all()
    )

    if len(chat_user_list_arr) != 1:
        raise RuntimeError("Unexpectedly much rows was transformed or acquired")
    chat_user_list = chat_user_list_arr[0]

    chat_data_arr = (
        conn.execute(select(chat_db).where(chat_db.c.id == chat_id)).mappings().all()
    )
    if len(chat_data_arr) != 1:
        raise RuntimeError("Unexpectedly much rows was transformed or acquired")
    chat_data = chat_data_arr[0]
    # Probably, chat_user_list may be none?!

    return Chat(
        id=chat_data["id"],
        name=chat_data["name"],
        user_id_list=chat_user_list["user_id_list="],
    )


def create_chat_db(
    conn: ConnectionDep, chat_create: ChatCreate, user_token: TokenData
) -> Chat:
    # Verify chat creator belong to chat_create.user_id_list
    if user_token.user_id not in chat_create.user_id_list:
        chat_create.user_id_list.append(user_token.user_id)

    try:
        chat_main_data_arr = (
            conn.execute(
                insert(chat_db).values({"name": chat_create.name}).returning(chat_db)
            )
            .mappings()
            .all()
        )
    except IntegrityError:
        raise DuplicateError(f"Creating chat {chat_create.name} is already exists")

    if len(chat_main_data_arr) != 1:
        raise RuntimeError("Unexpectedly much rows was transformed or acquired")
    chat_main_data = chat_main_data_arr[0]

    chat_user_data = (
        conn.execute(
            insert(chat_user_db).returning(chat_user_db),
            parameters=[
                {
                    "chat_id": chat_main_data["id"],
                    "user_info_id": user_id,
                }
                for user_id in chat_create.user_id_list
            ],
        )
        .mappings()
        .all()
    )
    if len(chat_user_data) != len(chat_create.user_id_list):
        raise RuntimeError("Unexpectedly much rows was transformed or acquired")

    return Chat(
        id=chat_main_data["id"],
        name=chat_main_data["name"],
        user_id_list=chat_create.user_id_list,
    )
