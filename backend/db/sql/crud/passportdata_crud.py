from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.sql.models import PassportsData

class PassportDataCRUD:
    async def create(self, db: AsyncSession, passport_data: dict) -> PassportsData:
        db_passport = PassportsData(**passport_data) # TODO сделать обновление пользователя на имя, фамилию и отчество и добавить этого пользователя в таблицу ConfirmPassportData для подтверждения личности
        db.add(db_passport)
        await db.commit()
        await db.refresh(db_passport)
        return db_passport

    async def get(self, db: AsyncSession, passport_id: int) -> Optional[PassportsData]:
        result = await db.execute(select(PassportsData).where(PassportsData.id == passport_id))
        return result.scalar_one_or_none()

    async def get_by_user(self, db: AsyncSession, user_id: int) -> Optional[PassportsData]:
        result = await db.execute(select(PassportsData).where(PassportsData.user_id == user_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, passport_id: int, update_data: dict) -> Optional[PassportsData]:
        result = await db.execute(
            update(PassportsData)
            .where(PassportsData.id == passport_id)
            .values(**update_data, updated_at=datetime.utcnow())
        )
        if result.rowcount == 0:
            return None
        await db.commit()
        return await self.get(db, passport_id)

    async def delete(self, db: AsyncSession, passport_id: int) -> bool:
        result = await db.execute(delete(PassportsData).where(PassportsData.id == passport_id))
        await db.commit()
        return result.rowcount > 0

    async def delete_by_user(self, db: AsyncSession, user_id: int) -> bool:
        result = await db.execute(delete(PassportsData).where(PassportsData.user_id == user_id))
        await db.commit()
        return result.rowcount > 0