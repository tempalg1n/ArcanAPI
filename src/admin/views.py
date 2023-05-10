from sqladmin import ModelView

from src.cards.models import arcane, user


class ArcaneAdmin(ModelView, model=arcane):
    column_list = [c.name for c in arcane.__table__.c]
    name = 'Arcane'
    name_plural = 'Arcanes'
    icon = "fa-solid fa-cards"


class UsersAdmin(ModelView, model=user):
    column_list = [user.c.email, user.c.username]
    column_details_exclude_list = [user.c.hashed_password]
    can_delete = False
    name = 'User'
    name_plural = 'Users'
    icon = "fa-solid fa-user"
