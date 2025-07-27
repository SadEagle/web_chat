from sqlalchemy.exc import IntegrityError
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
    UserListAdapter,
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
        user_result = (
            conn.execute(
                insert(user_db).returning(user_db).values(user.model_dump(mode="json"))
            )
            .mappings()
            .one()
        )
    except IntegrityError:
        raise DuplicateError("Login or email already in use")

    if user_result is None:
        return None
    return User.model_validate(user_result)


def update_user_db(conn: ConnectionDep, user_update: UserUpdate) -> User | None:
    if user_update.passwd is None:
        user_update_secure = UserUpdateSecure(**user_update.model_dump())
    else:
        user_update_secure = UserUpdateSecure(
            **user_update.model_dump(),
            hashed_passwd=get_passwd_hash(user_update.passwd),
        )

    try:
        updated_user = (
            conn.execute(
                update(user_db)
                .where(user_db.c.id == user_update.id)
                .returning(user_db)
                .values(
                    user_update_secure.model_dump(exclude_defaults=True, mode="json")
                )
            )
            .mappings()
            .one_or_none()
        )
    except IntegrityError as exc:
        raise DuplicateError(f"Cant update user")

    if updated_user is None:
        return None

    return User.model_validate(updated_user)


def get_user_by_name_db(conn: ConnectionDep, user_name: str) -> User | None:
    user_result = (
        conn.execute(select(user_db).where(user_db.c.login == user_name))
        .mappings()
        .one_or_none()
    )

    if user_result is None:
        return None

    return User.model_validate(user_result)


def get_current_user_by_id(conn: ConnectionDep, user_id: int) -> User | None:
    current_user = (
        conn.execute(select(user_db).where(user_db.c.id == user_id))
        .mappings()
        .one_or_none()
    )
    if current_user is None:
        return None
    return User.model_validate(current_user)


def get_users_by_id_db(conn: ConnectionDep, user_id_list: list[int]) -> list[User]:
    users_result = (
        conn.execute(select(user_db).where(user_db.c.id.in_(user_id_list)))
        .mappings()
        .all()
    )

    if len(users_result) == 0:
        return []
    return UserListAdapter.validate_python(users_result)
