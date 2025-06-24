"""Database operations

Database and all crud operations
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
