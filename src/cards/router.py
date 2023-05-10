from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from src.auth.base_config import current_active_user
from src.auth.database import User
from src.cards.models import arcane
from src.cards.schemas import ArcaneBaseSchema
from src.database import get_async_session


router = APIRouter()


@router.get('/', description='Get all the arcanes, total is 78')
@cache(expire=30)
async def get_arcanes(db: Session = Depends(get_async_session),
                      limit: int = 10, page: int = 1, type: str = ''):
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
    return {
        "status": "success",
        "data": data,
        "details": None
    }


@router.get('/{slug_name}', description="Get certain arcane by it's name. For example 'fool', 'emperor', "
                                        "'ten_of_wands', etc.")
async def get_arcane(slug_name: str, db: Session = Depends(get_async_session)):
    query = select(arcane).where(arcane.c.slug == slug_name)
    results = await db.execute(query)
    data = list(results.mappings())
    if data:
        return {
            "status": "success",
            "arcane": data
        }
    else:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "details": f"Arcane {slug_name} not found"
        })


@router.post("")
async def add_new_arcane(new_arcane: ArcaneBaseSchema,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    stmt = insert(arcane).values(**new_arcane.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.patch('/{slug_name}')
async def update_arcane_info(slug_name: str,
                             payload: ArcaneBaseSchema,
                             user: User = Depends(current_active_user),
                             db: Session = Depends(get_async_session)):
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


@router.delete('/{slug_name}')
async def delete_arcane(slug_name: str,
                        db: Session = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
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
