from datetime import datetime

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, JSON, ForeignKey, Boolean, ARRAY
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()


class Base(DeclarativeBase):
    pass


role = Table(
    "role",
    metadata,
    Column("id", primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
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


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     username = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP, default=datetime.utcnow())
#     role_id = Column(Integer, ForeignKey(role.c.id))
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#
#     __table_args__ = {'extend_existing': True}

class User(Base):
    __table__ = user


class Arcane(Base):
    __table__ = arcane

# class Arcane(Base):
#     __tablename__ = 'arcane'
#     id = Column(Integer, primary_key=True)
#     type = Column(String, nullable=False)
#     name = Column(String, nullable=False)
#     slug = Column(String, nullable=False)
#     card = Column(String, nullable=True)
#     brief = Column(ARRAY(String))
#     general = Column(String, nullable=True)
#     personal_condition = Column(String, nullable=True)
#     deep = Column(String, nullable=True)
#     career = Column(String, nullable=True)
#     finances = Column(String, nullable=True)
#     relations = Column(String, nullable=True)
#     upside_down = Column(String, nullable=True)
#     combination = Column(String, nullable=True)
#     archetypal = Column(String, nullable=True)
#     health = Column(String, nullable=True)
#     remarks = Column(String, nullable=True)
#
#     __table_args__ = {'extend_existing': True}
