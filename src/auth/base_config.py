from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport

from src.auth.database import User
from src.auth.manager import get_user_manager

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

SECRET = 'peepeepoopoo'


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_active_user = users.current_user(active=True)
