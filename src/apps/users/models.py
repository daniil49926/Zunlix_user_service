import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.core.db.database import Base
from src.core.settings import settings


class User(Base):
    __tablename__ = "User"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    surname: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False, unique=True)
    gender: int = Column(Integer, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
    created_at: datetime.datetime = Column(DateTime, default=datetime.datetime.now())
    is_active: int = Column(
        Integer, nullable=False, default=0 if not settings.TESTING else 1
    )
