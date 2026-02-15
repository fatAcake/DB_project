from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_postgres_db
from services.users_service import UsersService
from db.sql.schemas.users_schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Создание пользователя"""
    service = UsersService(session)
    return await service.create(data)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_postgres_db),
):
    """Получение списка пользователей"""
    service = UsersService(session)
    return await service.get_all(skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Получение пользователя по ID"""
    service = UsersService(session)
    return await service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Обновление пользователя"""
    service = UsersService(session)
    return await service.update(user_id, data)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Удаление пользователя"""
    service = UsersService(session)
    await service.delete(user_id)
    return {"ok": True}
