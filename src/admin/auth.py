from typing import Optional

from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.base_config import current_active_user
from src.auth.database import get_user_db
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead
from src.database import get_async_session


async def read_user(email: str, password: str):
    try:
        async with get_async_session() as session:
            async with get_user_db(session) as user_db:
                async with get_user_manager(user_db) as user_manager:
                    user = await user_manager.read(
                        UserRead(
                            email=email, password=password
                        )
                    )
                    print(f"User {user}")
                    return user


    except Exception:
        print('no such user')


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["email"], form["password"]
        user = await read_user(email=email, password=password)
        if user:
            pass

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


authentication_backend = AdminAuth(secret_key="...")
