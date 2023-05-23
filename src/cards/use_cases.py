from typing import AsyncIterator

from fastapi import HTTPException

from src.cards.response_models import ArcaneSchema
from src.models import Arcane, AsyncSession


class ReadArcane:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, slug_name: str) -> ArcaneSchema:
        async with self.async_session() as session:
            arcane = await Arcane.read_by_slug(session, slug_name)
            if not arcane:
                raise HTTPException(status_code=404)
            return ArcaneSchema.from_orm(arcane)


class ReadAllArcanes:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, page, limit, type) -> AsyncIterator[ArcaneSchema]:
        async with self.async_session() as session:
            async for arcane in Arcane.read_all(session, page, limit, type):
                yield ArcaneSchema.from_orm(arcane)
