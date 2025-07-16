from sqlalchemy.exc import IntegrityError
from pydantic import TypeAdapter
from sqlalchemy import (
    insert,
    update,
    select,
)

from app.data_model.user_model import (
    UserCreate,
    UserCreateSecure,
    UserUpdate,
    User,
    UserUpdateSecure,
)

from app.data_model.db_model import user_db
from app.deps import ConnectionDep
from app.exceptions import DuplicateError
from app.core.secret import get_passwd_hash


def create_user_db(conn: ConnectionDep, user_create: UserCreate) -> User | None:
    user = UserCreateSecure(
        **user_create.model_dump(),
        hashed_passwd=get_passwd_hash(user_create.passwd),
    )

    try:
        user_result_arr = (
            conn.execute(
                insert(user_db).returning(user_db).values(user.model_dump(mode="json"))
            )
            .mappings()
            .all()
        )
    except IntegrityError as exc:
        raise DuplicateError("Login or email already in use")

    if len(user_result_arr) != 1:
        raise RuntimeError("Unexpectedly much rows was transformed or acquired")
    user_result = user_result_arr[0]

    if user_result is None:
        return None
    return User.model_validate(user_result)


def update_user_db(conn: ConnectionDep, user_update: UserUpdate) -> User | None:
    if user_update.passwd is None:
        hashed_passwd = None
    else:
        hashed_passwd = get_passwd_hash(user_update.passwd)
    user_update_secure = UserUpdateSecure(
        **user_update.model_dump(),
        hashed_passwd=hashed_passwd,
    )
    try:
        updated_users = (
            conn.execute(
                update(user_db)
                .where(user_db.c.id == user_update.id)
                .returning(user_db)
                .values(
                    user_update_secure.model_dump(exclude_defaults=True, mode="json")
                )
            )
            .mappings()
            .all()
        )
    except IntegrityError as exc:
        if "email" in str(exc).lower():
            raise DuplicateError(f"Email '{user_update.email}' already exists")
        else:
            raise DuplicateError("Unexpected column duplicate")

    if len(updated_users) == 0:
        return None
    elif len(updated_users) == 1:
        update_user_result = updated_users[0]
    else:
        # Impossible to achive
        raise RuntimeError("Unexpectedly much rows was transformed or acquired")

    if update_user_result is None:
        return None
    return User.model_validate(update_user_result)


def get_user_db(conn: ConnectionDep, user_name: str) -> User | None:
    users_result = (
        conn.execute(select(user_db).where(user_db.c.login == user_name))
        .mappings()
        .all()
    )

    if len(users_result) == 0:
        return None
    elif len(users_result) == 1:
        user = users_result[0]
    else:
        raise RuntimeError("Unexpectedly much rows was transformed or acquired")

    return User.model_validate(user)
