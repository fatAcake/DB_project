from datetime import datetime
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from db.sql.models import ConfirmPassportData
from db.sql.schemas.confirm_passport_data_schemas import ConfirmPassportDataCreate, ConfirmPassportDataUpdate


async def create_confirm_passport_data(session: AsyncSession, data: ConfirmPassportDataCreate) -> ConfirmPassportData | None:
    """Создание подтверждения паспортных данных"""
    try:
        confirm_passport_data = ConfirmPassportData(**data.model_dump())
        session.add(confirm_passport_data)
        await session.commit()
        await session.refresh(confirm_passport_data)
        return confirm_passport_data
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка создания подтверждения паспортных данных",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def get_confirm_passport_data(session: AsyncSession, confirm_passport_data_id: int) -> ConfirmPassportData | None:
    """Получение подтверждения паспортных данных по ID"""
    try:
        result = await session.execute(
            select(ConfirmPassportData).where(ConfirmPassportData.id == confirm_passport_data_id)
        )
        confirm_passport_data = result.scalar_one_or_none()
        return confirm_passport_data
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения подтверждения паспортных данных",
            "confirm_passport_data_id": confirm_passport_data_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def get_confirm_passport_datas(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[ConfirmPassportData] | None:
    """Получение списка подтверждений паспортных данных"""
    try:
        result = await session.execute(
            select(ConfirmPassportData)
            .offset(skip)
            .limit(limit)
        )
        confirm_passport_datas = result.scalars().all()
        return list(confirm_passport_datas)
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения списка подтверждений паспортных данных",
            "skip": skip,
            "limit": limit,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def update_confirm_passport_data(session: AsyncSession, confirm_passport_data_id: int,  data: ConfirmPassportDataUpdate) -> ConfirmPassportData | None:
    """Обновление подтверждения паспортных данных"""
    try:
        confirm_passport_data = await get_confirm_passport_data(session, confirm_passport_data_id)
        if not confirm_passport_data:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(confirm_passport_data, field, value)
        
        await session.commit()
        await session.refresh(confirm_passport_data)
        return confirm_passport_data
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка обновления подтверждения паспортных данных",
            "confirm_passport_data_id": confirm_passport_data_id,
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def delete_confirm_passport_data(session: AsyncSession, confirm_passport_data_id: int) -> bool:
    """Удаление подтверждения паспортных данных"""
    try:
        result = await session.execute(
            delete(ConfirmPassportData).where(ConfirmPassportData.id == confirm_passport_data_id)
        )
        await session.commit()
        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка удаления подтверждения паспортных данных",
            "confirm_passport_data_id": confirm_passport_data_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return False