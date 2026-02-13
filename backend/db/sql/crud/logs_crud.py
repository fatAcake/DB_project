from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.sql.models import Logs

class LogsCRUD:
    async def create(self, db: AsyncSession, log_data: dict) -> Logs:
        db_log = Logs(**log_data)
        db.add(db_log)
        await db.commit()
        await db.refresh(db_log)
        return db_log

    async def get(self, db: AsyncSession, log_id: int) -> Optional[Logs]:
        result = await db.execute(select(Logs).where(Logs.id == log_id))
        return result.scalar_one_or_none()

    async def get_by_user(self, db: AsyncSession, user_id: int) -> List[Logs]:
        result = await db.execute(
            select(Logs).where(Logs.user_id == user_id).order_by(Logs.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Logs]:
        result = await db.execute(
            select(Logs).offset(skip).limit(limit).order_by(Logs.created_at.desc())
        )
        return list(result.scalars().all())

    async def update(self, db: AsyncSession, log_id: int, update_data: dict) -> Optional[Logs]:
        result = await db.execute(
            update(Logs)
            .where(Logs.id == log_id)
            .values(**update_data, updated_at=datetime.utcnow())
        )
        if result.rowcount == 0:
            return None
        await db.commit()
        return await self.get(db, log_id)

    async def delete(self, db: AsyncSession, log_id: int) -> bool:
        result = await db.execute(delete(Logs).where(Logs.id == log_id))
        await db.commit()
        return result.rowcount > 0

    async def delete_by_user(self, db: AsyncSession, user_id: int) -> int:
        result = await db.execute(delete(Logs).where(Logs.user_id == user_id))
        await db.commit()
        return result.rowcount