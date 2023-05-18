from typing import AsyncIterator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.common.logs import logger
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL, echo=True
)


async_engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_async_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)
