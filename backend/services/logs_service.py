from typing import List
from fastapi import HTTPException
from db.session import AsyncSessionLocalPostgres
from db.sql.crud.logs_crud import LogsCRUD
from db.sql.schemas.logs_schema import LogCreate, LogUpdate
from db.sql.models import Logs

class LogsService:
    def __init__(self):
        self.crud = LogsCRUD()

    async def create_log(self, log_data: LogCreate) -> Logs:
        async with AsyncSessionLocalPostgres() as db:
            return await self.crud.create(db, log_data.model_dump())

    async def get_log(self, log_id: int) -> Logs:
        async with AsyncSessionLocalPostgres() as db:
            log = await self.crud.get(db, log_id)
            if not log:
                raise HTTPException(404, "Log not found")
            return log

    async def get_logs_by_user(self, user_id: int) -> List[Logs]:
        async with AsyncSessionLocalPostgres() as db:
            return await self.crud.get_by_user(db, user_id)

    async def get_all_logs(self, skip: int = 0, limit: int = 100) -> List[Logs]:
        async with AsyncSessionLocalPostgres() as db:
            return await self.crud.get_all(db, skip, limit)

    async def update_log(self, log_id: int, log_data: LogUpdate) -> Logs:
        async with AsyncSessionLocalPostgres() as db:
            log = await self.crud.get(db, log_id)
            if not log:
                raise HTTPException(404, "Log not found")
            update_dict = log_data.model_dump(exclude_unset=True)
            return await self.crud.update(db, log_id, update_dict)

    async def delete_log(self, log_id: int) -> bool:
        async with AsyncSessionLocalPostgres() as db:
            log = await self.crud.get(db, log_id)
            if not log:
                raise HTTPException(404, "Log not found")
            return await self.crud.delete(db, log_id)

    async def delete_logs_by_user(self, user_id: int) -> int:
        async with AsyncSessionLocalPostgres() as db:
            return await self.crud.delete_by_user(db, user_id)