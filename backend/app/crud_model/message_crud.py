from datetime import datetime
from pydantic import TypeAdapter
from sqlalchemy import insert, select, desc

from app.deps import ConnectionDep
from app.data_model.message_model import MessageCreate, Message, MessageBatch
from app.data_model.db_model import message_db


msg_adapter = TypeAdapter(list[Message])


def store_message_db(conn: ConnectionDep, message: MessageCreate) -> Message | None:
    message_data = message.model_dump(mode="json")
    message_result = conn.execute(
        insert(message_db).returning(message_db).values(message_data)
    )
    message_row = message_result.first()
    if message_row is None:
        return None
    return Message.model_validate(message_row._mapping)


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
