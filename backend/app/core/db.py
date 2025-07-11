from sqlalchemy import create_engine

from app.core.config import settings, RunMode
from app.core.base_db_model import metadata_obj

if settings.RUN_MODE == RunMode.PROD:
    engine = create_engine(settings.SQLALCHEMY_PROD_DB_URL)
elif settings.RUN_MODE == RunMode.DEV:
    engine = create_engine(settings.SQLALCHEMY_DEV_DB_URL, echo=True)
else:
    engine = create_engine(settings.SQLALCHEMY_TEST_DB_URL, echo=True)
metadata_obj.create_all(engine)
