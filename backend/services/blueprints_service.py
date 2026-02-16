from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.sql.crud.blueprints_crud import (
    create_blueprint, get_blueprint, get_blueprints,
    update_blueprint, delete_blueprint
)
from db.sql.schemas.blueprints_schemas import BlueprintCreate, BlueprintUpdate, BlueprintInfo


class BlueprintsService:
    """Сервис для работы с чертежами"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: BlueprintCreate) -> BlueprintInfo:
        """Создание чертежа"""
        blueprint = await create_blueprint(self.session, data)
        if not blueprint:
            raise HTTPException(400, "Failed to create blueprint")
        
        return BlueprintInfo(
            id=blueprint.id,
            name=blueprint.name,
            description=blueprint.description
        )

    async def get_by_id(self, blueprint_id: int) -> BlueprintInfo:
        """Получение чертежа по ID"""
        blueprint = await get_blueprint(self.session, blueprint_id)
        if not blueprint:
            raise HTTPException(404, "Blueprint not found")
        
        return BlueprintInfo(
            id=blueprint.id,
            name=blueprint.name,
            description=blueprint.description
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[BlueprintInfo]:
        """Получение списка чертежей"""
        blueprints = await get_blueprints(self.session, skip, limit)
        if not blueprints:
            return []
        return [
            BlueprintInfo(
                id=blueprint.id,
                name=blueprint.name,
                description=blueprint.description
            )
            for blueprint in blueprints
        ]

    async def update(self, blueprint_id: int, data: BlueprintUpdate) -> BlueprintInfo:
        """Обновление чертежа"""
        blueprint = await update_blueprint(self.session, blueprint_id, data)
        if not blueprint:
            raise HTTPException(404, "Blueprint not found")
        
        return BlueprintInfo(
            id=blueprint.id,
            name=blueprint.name,
            description=blueprint.description
        )

    async def delete(self, blueprint_id: int) -> bool:
        """Удаление чертежа"""
        success = await delete_blueprint(self.session, blueprint_id)
        if not success:
            raise HTTPException(404, "Blueprint not found")
        return True