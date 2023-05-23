import contextlib
from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.base_config import auth_backend, get_jwt_strategy
from src.auth.database import get_user_db
from src.auth.manager import get_user_manager
from src.config import SECRET_ADMIN
from src.database import get_admin_session

get_session_context = contextlib.asynccontextmanager(get_admin_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def read_user(email: str, password: str):
    async with get_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                credentials = OAuth2PasswordRequestForm(username=email, password=password, scope='')
                user = await user_manager.authenticate(credentials)
                return user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        user = await read_user(email=form['username'], password=form['password'])
        if user:
            auth = await auth_backend.login(get_jwt_strategy(), user)
            token = eval(auth.body.decode('utf-8'))['access_token']
            request.session.update({'token': token})
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


authentication_backend = AdminAuth(secret_key=SECRET_ADMIN)
