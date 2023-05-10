from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.auth.base_config import users, auth_backend
from src.cards.router import router as card_router

from src.auth.schemas import UserRead, UserCreate
from redis import asyncio as aioredis

app = FastAPI()

app.include_router(card_router,
                   tags=["Card"],
                   prefix="/arcane")

app.include_router(
    users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

app.include_router(
    users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=["auth"]
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")