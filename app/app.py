from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from sqladmin import Admin
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from admin.auth import authentication_backend
from admin.views import ArcaneAdmin, UsersAdmin, RoleAdmin
from auth.base_config import users, auth_backend
from cards.router import router as card_router

from auth.schemas import UserRead, UserCreate
from redis import asyncio as aioredis

from common.enums import RouteTag
from common.logs import logger
from config import REDIS_HOST, REDIS_PORT
from database import engine
from settings import settings

app = FastAPI(title='ArcanAPI')


def custom_openapi():  # pragma: no cover
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ArcanAPI",
        description="API that will give you detailed information about all known tarot arcana",
        version=settings.app_version,
        contact={
            "name": 'Ivan "clappingseal" Muranov',
            "url": "https://github.com/tempalg1n/ArcanAPI",
            "email": "ivanmuranov595@gmail.com",
        },
        license_info={
            "name": "MIT",
        },
        routes=app.routes,
        tags=[
            {
                "name": RouteTag.ARCANES,
                "description": "Info about tarot arcanes",
            },
            {
                "name": RouteTag.AUTH,
                "description": "Registration and authorization",
            },
        ],
        #        servers=[{"url": settings.app_base_url, "description": "Production server"}],
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://files.tekrop.fr/overfast_api_logo_full_1000.png",
    #     "altText": "OverFast API Logo",
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.logger = logger
logger.info("ArcanAPI... Online !")
logger.info("Version : {}", settings.app_version)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)


# We need to override default Redoc page in order to be
# able to customize the favicon, same for Swagger
common_doc_settings = {
    # "openapi_url": app.openapi_url,
    "title": f"{settings.title} - Documentation",
    "favicon_url": "app/static/favicon.png",
}


@app.get("/", include_in_schema=False)
async def overridden_redoc():
    redoc_settings = common_doc_settings.copy()
    redoc_settings["redoc_favicon_url"] = redoc_settings.pop("favicon_url")
    return get_redoc_html(**redoc_settings)


@app.get("/docs", include_in_schema=False)
async def overridden_swagger():
    swagger_settings = common_doc_settings.copy()
    swagger_settings["swagger_favicon_url"] = swagger_settings.pop("favicon_url")
    return get_swagger_ui_html(**swagger_settings)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(ArcaneAdmin)
admin.add_view(UsersAdmin)
admin.add_view(RoleAdmin)

app.include_router(card_router,
                   prefix="/arcane")

app.include_router(
    users.get_auth_router(auth_backend),
    tags=[RouteTag.AUTH],
    prefix="/auth/jwt"
)

app.include_router(
    users.get_register_router(UserRead, UserCreate),
    tags=[RouteTag.AUTH],
    prefix='/auth'
)
