from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import Connection

from app.core.db import engine


def get_db() -> Generator[Connection, None, None]:
    with engine.begin() as conn:
        yield conn


ConnectionDep = Annotated[Connection, Depends(get_db)]
