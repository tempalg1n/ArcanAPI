from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi_cache.decorator import cache
from starlette import status

from src.cards.response_models import ArcaneSchema, AllArcanesSchema
from src.cards.use_cases import ReadAllArcanes, ReadArcane
from src.common.enums import RouteTag, ArcanesNames, ArcanesTypes
from src.common.errors_models import ArcaneNotFoundMessage
from src.common.helpers import routes_responses


router = APIRouter()


@router.get('/',
            description='Get all the arcanes, total is 78',
            tags=[RouteTag.ARCANES],
            responses=routes_responses,
            response_model=AllArcanesSchema
            )
@cache(expire=30)
async def get_arcanes(
        limit: int = 10,
        page: int = 1,
        type: ArcanesTypes | None = Query(
            None, title="Type of arcane (minor of major)", example='major'),
        use_case: ReadAllArcanes = Depends(ReadAllArcanes)
):
    return AllArcanesSchema(arcanes=[arcane async for arcane in use_case.execute(page, limit, type)])


@router.get('/{slug_name}',
            description="Get certain arcane by it's name. For example 'fool', 'emperor', "
                        "'ten_of_wands', etc.",
            tags=[RouteTag.ARCANES],
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": ArcaneNotFoundMessage,
                    "description": "Arcane not found"
                },
                **routes_responses},
            response_model=ArcaneSchema)
async def get_arcane(
        slug_name: ArcanesNames = Path(title='Key name of arcane'),
        use_case: ReadArcane = Depends(ReadArcane)
):
    data: ArcaneSchema = await use_case.execute(slug_name=slug_name)
    return data
