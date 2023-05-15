from datetime import datetime

from sqlalchemy import Column, Integer, Table, String, TIMESTAMP, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import DeclarativeBase

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


class Role(Base):
    __table__ = role


class User(Base):
    __table__ = user
