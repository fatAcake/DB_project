from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_postgres_db
from services.confirm_passport_data_service import ConfirmPassportDataService
from db.sql.schemas.confirm_passport_data_schemas import ConfirmPassportDataCreate, ConfirmPassportDataUpdate, ConfirmPassportDataInfo

router = APIRouter(
    prefix="/confirm-passport-data",
    tags=["Confirm Passport Data"]
)


@router.post("/", response_model=ConfirmPassportDataInfo)
async def create_confirm_passport_data(
    data: ConfirmPassportDataCreate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Создание нового подтверждения паспортных данных"""
    service = ConfirmPassportDataService(session)
    return await service.create(data)


@router.get("/{confirm_passport_data_id}", response_model=ConfirmPassportDataInfo)
async def get_confirm_passport_data(
    confirm_passport_data_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение подтверждения паспортных данных по ID"""
    service = ConfirmPassportDataService(session)
    return await service.get_by_id(confirm_passport_data_id)


@router.get("/", response_model=List[ConfirmPassportDataInfo])
async def get_confirm_passport_datas(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение списка подтверждений паспортных данных"""
    service = ConfirmPassportDataService(session)
    return await service.get_all(skip, limit)


@router.put("/{confirm_passport_data_id}", response_model=ConfirmPassportDataInfo)
async def update_confirm_passport_data(
    confirm_passport_data_id: int,
    data: ConfirmPassportDataUpdate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Обновление подтверждения паспортных данных"""
    service = ConfirmPassportDataService(session)
    return await service.update(confirm_passport_data_id, data)


@router.delete("/{confirm_passport_data_id}")
async def delete_confirm_passport_data(
    confirm_passport_data_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Удаление подтверждения паспортных данных"""
    service = ConfirmPassportDataService(session)
    await service.delete(confirm_passport_data_id)
    return {"message": "Confirm passport data deleted successfully", "confirm_passport_data_id": confirm_passport_data_id, "status_code": 200}