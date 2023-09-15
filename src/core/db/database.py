from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

DATABASE_URL = settings.PG_DSN

CONNECT_TRY = settings.MAX_ATTEMPTS_TO_CONN_TO_PG
if not settings.TESTING:
    engine = create_async_engine("postgresql+asyncpg://" + DATABASE_URL, echo=True)
    async_session = sessionmaker(engine=engine, expire_on_commit=False, class_=AsyncSession)
else:
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)
    async_session = sessionmaker(engine=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> Generator:
    db = async_session()
    yield db
