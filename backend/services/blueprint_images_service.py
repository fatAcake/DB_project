from typing import List
from fastapi import UploadFile, HTTPException

from db.nosql.crud.blueprint_images import BlueprintsCRUD
from db.nosql.models import Blueprint


class BlueprintsService:
    """Сервис для чертежей"""
    
    def __init__(self, crud: BlueprintsCRUD):
        self.crud = crud
    
    async def upload_blueprint(
        self,
        file: UploadFile,
        blueprint_id_sql: int
    ) -> Blueprint:
        """Загрузка чертежа"""
        # Валидация размера
        file_data = await file.read()
        if len(file_data) > 16 * 1024 * 1024:
            raise HTTPException(400, "File size exceeds 16MB limit (MongoDB document size limit)")
        
        return await self.crud.create(
            file_data=file_data,
            filename=file.filename or "unknown",
            blueprint_id_sql=blueprint_id_sql,
            content_type=file.content_type or "application/octet-stream"
        )
    
    async def get_blueprint(self, blueprint_id: str) -> Blueprint:
        """Получение чертежа"""
        blueprint = await self.crud.get(blueprint_id)
        if not blueprint:
            raise HTTPException(404, "Blueprint not found")
        return blueprint
    
    async def get_blueprints(self) -> list:
        """Получение всех чертежей"""
        return await self.crud.get_all()
    
    async def get_blueprint_versions(self, blueprint_id_sql: int) -> List[Blueprint]:
        """Получение всех чертежей для записи"""
        return await self.crud.get_by_blueprint_sql(blueprint_id_sql)
    
    async def delete_blueprint(self, blueprint_id: str) -> bool:
        """Удаление чертежа"""
        blueprint = await self.crud.get(blueprint_id)
        if not blueprint:
            raise HTTPException(404, "Blueprint not found")
        return await self.crud.delete(blueprint_id)
    
    async def delete_blueprint_versions(self, blueprint_id_sql: int) -> int:
        """Удаление всех чертежей для записи"""
        return await self.crud.delete_by_blueprint_sql(blueprint_id_sql)