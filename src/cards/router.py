from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from src.auth.base_config import current_active_user
from src.auth.database import User
from src.cards.schemas import ArcaneBaseSchema, ArcanesResponse
from src.common.api_examples import single_arcane_example, responses, all_arcanes_example
from src.common.enums import RouteTag, ArcanesNames, ArcanesTypes
from src.database import get_async_session
from src.models import arcane

router = APIRouter()


@router.get('/',
            description='Get all the arcanes, total is 78',
            tags=[RouteTag.ARCANES],
            response_model=ArcanesResponse,
            responses={**responses, 200: {"content": all_arcanes_example}}
            )
@cache(expire=30)
async def get_arcanes(
        db: Session = Depends(get_async_session),
        limit: int = 10,
        page: int = 1,
        type: ArcanesTypes | None = Query(
            None, title="Type of arcane (minor of major)", example='major')
):
    skip = (page - 1) * limit
    if type:
        if type in ['minor', 'major']:
            query = arcane.select().offset(skip).limit(limit).where(arcane.c.type == type).order_by(arcane.c.id)
        else:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Arcane type {type} does not exist"
            })
    else:
        query = arcane.select().offset(skip).limit(limit)
    results = await db.execute(query)
    data = list(results.mappings())
    if data:
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    else:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "details": f"No such arcane"
        })


@router.get('/{slug_name}',
            description="Get certain arcane by it's name. For example 'fool', 'emperor', "
                        "'ten_of_wands', etc.",
            tags=[RouteTag.ARCANES],
            response_model=ArcanesResponse,
            responses={**responses, 200: {"content": single_arcane_example}})
async def get_arcane(
        slug_name: ArcanesNames = Path(title='Key name of arcane'),
        db: Session = Depends(get_async_session)
):
    query = select(arcane).where(arcane.c.slug == slug_name)
    results = await db.execute(query)
    data = list(results.mappings())
    if data:
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    else:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "details": f"Arcane {slug_name} not found"
        })


@router.post("", tags=[RouteTag.ARCANES],
             description='Add new arcane. Only admin of superuser allowed. Also, why do you need that? There is '
                         'already all of them.')
async def add_new_arcane(new_arcane: ArcaneBaseSchema,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    if user.is_superuser:
        stmt = insert(arcane).values(**new_arcane.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success",
                "data": None,
                "details": None}
    else:
        raise HTTPException(status_code=403, detail={
            "status": "error",
            "data": None,
            "details": f"You have no access to that operation"
        })


@router.patch('/{slug_name}', tags=[RouteTag.ARCANES],
              description='Update arcane info. Only admin of superuser allowed.')
async def update_arcane_info(slug_name: str,
                             payload: ArcaneBaseSchema,
                             user: User = Depends(current_active_user),
                             db: Session = Depends(get_async_session)):
    if user.is_superuser:
        query = select(arcane).where(arcane.c.slug == slug_name)
        results = await db.execute(query)
        data = list(results.mappings())
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f' Arcane {arcane} not found')
        stmt = update(arcane).where(arcane.c.slug == slug_name).values(**payload.dict())
        result = await db.execute(stmt)
        data = list(result.mappings())
        return {
            "status": "success",
            "data": data,
            "details": "Arcane info updated"
        }
    else:
        raise HTTPException(status_code=403, detail={
            "status": "error",
            "data": None,
            "details": f"You have no access to that operation"
        })


@router.delete('/{slug_name}', tags=[RouteTag.ARCANES],
               description='Delete one. Only admin of superuser allowed.')
async def delete_arcane(slug_name: str,
                        db: Session = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
    if user.is_superuser:
        query = select(arcane).where(arcane.c.slug == slug_name)
        results = await db.execute(query)
        data = list(results.mappings())
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f' Arcane {arcane} not found')
        stmt = delete(arcane).where(arcane.c.slug == slug_name)
        await db.execute(stmt)
        return {
            "status": "success",
            "data": data,
            "details": f"Arcane {slug_name} was deleted"
        }
    else:
        raise HTTPException(status_code=403, detail={
            "status": "error",
            "data": None,
            "details": f"You have no access to that operation"
        })
