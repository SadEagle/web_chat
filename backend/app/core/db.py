from sqlalchemy import create_engine, engine

from app.core.config import settings
from app.core.base_model_db import metadata_obj


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
metadata_obj.create_all(engine)
