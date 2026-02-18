from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_postgres_db
from services.users_service import UsersService
from db.sql.schemas.users_schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    PasswordSendCodeRequest,
    PasswordChangeRequest,
)

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


@router.get("/{user_id}/verification")
async def verification_user(
    user_id: int,
    verification_code: int = Query(..., description="Код подтверждения"),
    session: AsyncSession = Depends(get_postgres_db),
):
    """Верификация пользователя по коду"""
    service = UsersService(session)
    success = await service.verification_user(user_id, verification_code)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный код верификации или код истек"
        )
    
    return {"success": True, "message": "Пользователь успешно верифицирован"}


@router.post("/{user_id}/password/send-code")
async def send_password_code(
    user_id: int,
    body: Optional[PasswordSendCodeRequest] = None,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Отправить код смены пароля на email пользователя. Опционально: current_password для проверки."""
    service = UsersService(session)
    current = body.current_password if body else None
    await service.request_password_code(user_id, current_password=current)
    return {"success": True, "message": "Код отправлен на вашу почту"}


@router.post("/{user_id}/password/change")
async def change_password(
    user_id: int,
    data: PasswordChangeRequest,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Сменить пароль по коду из письма."""
    service = UsersService(session)
    await service.change_password(user_id, data)
    return {"success": True, "message": "Пароль успешно изменён"}