from datetime import datetime

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped


from database import get_async_session
from models import Base, role


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow())
    role_id = Column(Integer, ForeignKey(role.c.id))
    email: str = Column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = Column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = Column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = Column(
        Boolean, default=False, nullable=False
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

