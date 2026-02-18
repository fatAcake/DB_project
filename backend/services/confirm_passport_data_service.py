from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.sql.crud.confirm_passport_data_crud import (
    create_confirm_passport_data, get_confirm_passport_data, get_confirm_passport_datas,
    update_confirm_passport_data, delete_confirm_passport_data
)
from db.sql.schemas.confirm_passport_data_schemas import ConfirmPassportDataCreate, ConfirmPassportDataUpdate, ConfirmPassportDataInfo


class ConfirmPassportDataService:
    """Сервис для работы с подтверждением паспортных данных"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ConfirmPassportDataCreate) -> ConfirmPassportDataInfo:
        """Создание подтверждения паспортных данных"""
        confirm_passport_data = await create_confirm_passport_data(self.session, data)
        if not confirm_passport_data:
            raise HTTPException(400, "Failed to create confirm passport data")
        
        return ConfirmPassportDataInfo(
            id=confirm_passport_data.id,
            passport_data_id=confirm_passport_data.passport_data_id,
            is_confirm=confirm_passport_data.is_confirm
        )

    async def get_by_id(self, confirm_passport_data_id: int) -> ConfirmPassportDataInfo:
        """Получение подтверждения паспортных данных по ID"""
        confirm_passport_data = await get_confirm_passport_data(self.session, confirm_passport_data_id)
        if not confirm_passport_data:
            raise HTTPException(404, "Confirm passport data not found")
        
        return ConfirmPassportDataInfo(
            id=confirm_passport_data.id,
            passport_data_id=confirm_passport_data.passport_data_id,
            is_confirm=confirm_passport_data.is_confirm
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ConfirmPassportDataInfo]:
        """Получение списка подтверждений паспортных данных"""
        confirm_passport_datas = await get_confirm_passport_datas(self.session, skip, limit)
        if not confirm_passport_datas:
            raise HTTPException(404, "No confirm passport data found")
        
        return [
            ConfirmPassportDataInfo(
                id=confirm_passport_data.id,
                passport_data_id=confirm_passport_data.passport_data_id,
                is_confirm=confirm_passport_data.is_confirm
            )
            for confirm_passport_data in confirm_passport_datas
        ]

    async def update(self, confirm_passport_data_id: int, data: ConfirmPassportDataUpdate) -> ConfirmPassportDataInfo:
        """Обновление подтверждения паспортных данных"""
        confirm_passport_data = await update_confirm_passport_data(self.session, confirm_passport_data_id, data)
        if not confirm_passport_data:
            raise HTTPException(404, "Confirm passport data not found")
        
        return ConfirmPassportDataInfo(
            id=confirm_passport_data.id,
            passport_data_id=confirm_passport_data.passport_data_id,
            is_confirm=confirm_passport_data.is_confirm
        )

    async def delete(self, confirm_passport_data_id: int) -> bool:
        """Удаление подтверждения паспортных данных"""
        success = await delete_confirm_passport_data(self.session, confirm_passport_data_id)
        if not success:
            raise HTTPException(404, "Confirm passport data not found")
        return True