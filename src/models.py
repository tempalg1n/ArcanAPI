from datetime import datetime
from typing import AsyncGenerator, AsyncIterator

from fastapi import HTTPException
from sqlalchemy import Column, Integer, Table, String, TIMESTAMP, ForeignKey, Boolean, MetaData, select
from sqlalchemy.orm import DeclarativeBase

from src.cards.response_models import ArcaneSchema
from src.cards.use_cases import AsyncSession

metadata = MetaData()


class Base(DeclarativeBase):
    pass


role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("can_edit", Boolean, default=False, nullable=False),
    Column('can_edit_users', Boolean, default=False, nullable=False)
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False))

arcane = Table(
    "arcane",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String, nullable=False, default='minor'),
    Column("name", String, nullable=False),
    Column("slug", String, nullable=False),
    Column("card", String, nullable=False),
    Column("brief", String),
    Column("general", String),
    Column("personal_condition", String),
    Column("deep", String),
    Column("career", String),
    Column("finances", String),
    Column("relations", String),
    Column("upside_down", String),
    Column("combination", String),
    Column("archetypal", String),
    Column("health", String),
    Column("remarks", String)
)


class Arcane(Base):
    __table__ = arcane

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_slug(
            cls, session: AsyncSession, slug_name: str):
        stmt = select(cls).where(cls.slug == slug_name)
        return await session.scalar(stmt.order_by(cls.slug))


class Role(Base):
    __table__ = role


class User(Base):
    __table__ = user


class ReadArcane:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, slug_name: str) -> ArcaneSchema:
        async with self.async_session() as session:
            arcane = await Arcane.read_by_slug(session, slug_name)
            if not arcane:
                raise HTTPException(status_code=404)
            return ArcaneSchema.from_orm(arcane)
