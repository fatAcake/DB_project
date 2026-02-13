from fastapi import HTTPException
from db.session import AsyncSessionLocalPostgres
from db.sql.crud.passportdata_crud import PassportDataCRUD
from db.sql.schemas.passportdata_schema import PassportDataCreate, PassportDataUpdate
from db.sql.models import PassportsData

class PassportDataService:
    def __init__(self):
        self.crud = PassportDataCRUD()

    async def create_passport_data(self, passport_data: PassportDataCreate) -> PassportsData:
        async with AsyncSessionLocalPostgres() as db:
            existing = await self.crud.get_by_user(db, passport_data.user_id)
            if existing:
                raise HTTPException(400, "Passport data already exists for this user")
            return await self.crud.create(db, passport_data.model_dump())

    async def get_passport_data(self, passport_id: int) -> PassportsData:
        async with AsyncSessionLocalPostgres() as db:
            passport = await self.crud.get(db, passport_id)
            if not passport:
                raise HTTPException(404, "Passport data not found")
            return passport

    async def get_passport_data_by_user(self, user_id: int) -> PassportsData:
        async with AsyncSessionLocalPostgres() as db:
            passport = await self.crud.get_by_user(db, user_id)
            if not passport:
                raise HTTPException(404, "Passport data not found for this user")
            return passport

    async def update_passport_data(self, passport_id: int, passport_data: PassportDataUpdate) -> PassportsData:
        async with AsyncSessionLocalPostgres() as db:
            passport = await self.crud.get(db, passport_id)
            if not passport:
                raise HTTPException(404, "Passport data not found")
            update_dict = passport_data.model_dump(exclude_unset=True)
            return await self.crud.update(db, passport_id, update_dict)

    async def delete_passport_data(self, passport_id: int) -> bool:
        async with AsyncSessionLocalPostgres() as db:
            passport = await self.crud.get(db, passport_id)
            if not passport:
                raise HTTPException(404, "Passport data not found")
            return await self.crud.delete(db, passport_id)

    async def delete_passport_data_by_user(self, user_id: int) -> bool:
        async with AsyncSessionLocalPostgres() as db:
            return await self.crud.delete_by_user(db, user_id)