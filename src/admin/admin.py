from starlette_admin.contrib.sqla import Admin, ModelView

from src.app import app
from src.cards.models import arcane
from src.database import engine

admin = Admin(engine, title='ArcanAPI Admin')
admin.add_view(ModelView(arcane))
admin.mount_to(app)
