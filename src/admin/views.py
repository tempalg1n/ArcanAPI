from sqladmin import ModelView

from src.models import Arcane, User, Role


class ArcaneAdmin(ModelView, model=Arcane):
    column_list = [c.name for c in Arcane.__table__.c]
    column_formatters = {Arcane.card: lambda m, a: m.card[:10],
                         Arcane.brief: lambda m, a: m.brief[:20],
                         Arcane.general: lambda m, a: m.general[:20],
                         Arcane.personal_condition: lambda m, a: m.personal_condition[:20],
                         Arcane.deep: lambda m, a: m.deep[:20],
                         Arcane.career: lambda m, a: m.career[:20],
                         Arcane.finances: lambda m, a: m.finances[:20],
                         Arcane.relations: lambda m, a: m.relations[:20],
                         Arcane.upside_down: lambda m, a: m.upside_down[:20],
                         Arcane.combination: lambda m, a: m.combination[:20],
                         Arcane.archetypal: lambda m, a: m.archetypal[:20],
                         Arcane.health: lambda m, a: m.health[:20],
                         Arcane.remarks: lambda m, a: m.remarks[:20] if m.remarks else m.remarks}
    name = 'Arcane'
    name_plural = 'Arcanes'
    icon = "fa-solid fa-wand-magic-sparkles"


class UsersAdmin(ModelView, model=User):
    column_list = [User.email, User.username]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = 'User'
    name_plural = 'Users'
    icon = "fa-solid fa-user"


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.name, Role.can_edit, Role.can_edit_users]
    name = 'Roler'
    name_plural = 'Roles'
    icon = "fa-solid fa-users"
