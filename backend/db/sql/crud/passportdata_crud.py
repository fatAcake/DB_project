from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.sql.schemas.confirm_passport_data_schemas import ConfirmPassportDataCreate
from db.sql.models import PassportsData
from db.sql.crud.confirm_passport_data_crud import create_confirm_passport_data
# from db.sql.crud.users_crud import update
# from db.sql.crud.roles_crud import update
# from db.nosql.crud.blueprint_images import BlueprintsCRUD
# from db.nosql.crud.products_images import ProductsImagesCRUD

class PassportDataCRUD:
    async def create(self, db: AsyncSession, passport_data: dict) -> PassportsData:
        db_passport = PassportsData(**passport_data) # TODO сделать обновление Users на имя, фамилию и отчество
        db.add(db_passport)
        await db.commit()
        await db.refresh(db_passport)
        await create_confirm_passport_data(db, 
                                           ConfirmPassportDataCreate(
                                               passport_data_id=db_passport.id, 
                                               is_confirm=False))
        return db_passport

    async def get(self, db: AsyncSession, passport_id: int) -> Optional[PassportsData]:
        result = await db.execute(select(PassportsData).where(PassportsData.id == passport_id))
        return result.scalar_one_or_none()

    async def get_by_user(self, db: AsyncSession, user_id: int) -> Optional[PassportsData]:
        result = await db.execute(select(PassportsData).where(PassportsData.user_id == user_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, passport_id: int, update_data: dict) -> Optional[PassportsData]:
        # TODO при обновлении данных для пасспорта, имя, фамилия, отчество тоже должно измениться в Users
        # TODO если is_confirm = true то надо обновить роли для Users
        # TODO если при is_confirm = true были записи продуктов для продажи, а потом пользователь удалил свои паспортные данные, то удаляются и его продукты с маркетплейса
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
        #TODO если удаляется запись о паспорте то удаляются и продукты пользователя на маркетплейсе, потому что is_confirm = false
        result = await db.execute(delete(PassportsData).where(PassportsData.id == passport_id))
        await db.commit()
        return result.rowcount > 0
    
    async def delete_by_user(self, db: AsyncSession, user_id: int) -> bool:
        #TODO если удаляется запись о паспорте то удаляются и продукты пользователя на маркетплейсе, потому что is_confirm = false
        result = await db.execute(delete(PassportsData).where(PassportsData.user_id == user_id))
        await db.commit()
        return result.rowcount > 0