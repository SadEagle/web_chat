from typing import cast
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError

from app.exceptions import DuplicateError
from app.deps import ConnectionDep
from app.data_model.db_model import chat_user_db, chat_db
from app.data_model.chat_model import ChatCreate, Chat, ChatDelete, ChatListAdapter
from app.data_model.token_model import TokenData
from app.routes import user


def create_chat_db(
    conn: ConnectionDep, chat_create: ChatCreate, user_token: TokenData
) -> Chat:
    # Verify chat creator belong to chat_create.user_id_list
    if user_token.user_id not in chat_create.user_id_list:
        chat_create.user_id_list.append(user_token.user_id)

    try:
        inserted_chat = (
            conn.execute(
                insert(chat_db).values({"name": chat_create.name}).returning(chat_db)
            )
            .mappings()
            .one()
        )
    except IntegrityError:
        raise DuplicateError(f"Creating chat {chat_create.name} is already exists")

    conn.execute(
        insert(chat_user_db),
        parameters=[
            {
                "chat_id": inserted_chat["id"],
                "user_info_id": user_id,
            }
            for user_id in chat_create.user_id_list
        ],
    )

    return Chat(
        id=inserted_chat["id"],
        name=inserted_chat["name"],
        user_id_list=chat_create.user_id_list,
    )


def delete_chat_db(conn: ConnectionDep, chat_delete: ChatDelete) -> ChatDelete | None:
    deleted_chat = (
        conn.execute(delete(chat_db).where(chat_db.c.id == chat_delete.id))
        .mappings()
        .one_or_none()
    )
    if deleted_chat is None:
        return None
    return ChatDelete.model_validate(deleted_chat)


def get_current_user_chat_ids_db(conn: ConnectionDep, user_id: int) -> list[int]:
    """Get chat ids for current user"""
    current_user_chat_ids = (
        conn.execute(
            select(chat_user_db.c.chat_id).where(chat_user_db.c.user_info_id == user_id)
        )
        .scalars()
        .all()
    )
    return cast(list[int], current_user_chat_ids)


def get_chats_data_db(conn: ConnectionDep, chat_id_list: list[int]) -> list[Chat]:
    """Get list full chat data by chat id"""
    chats_list = (
        conn.execute(select(chat_db).where(chat_db.c.id.in_(chat_id_list)))
        .mappings()
        .all()
    )
    if len(chats_list) == 0:
        return []
    return ChatListAdapter.validate_python(chats_list)
