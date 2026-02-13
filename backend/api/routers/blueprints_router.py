from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_postgres_db
from services.blueprints_service import BlueprintsService
from db.sql.schemas.blueprints_schemas import BlueprintCreate, BlueprintUpdate, BlueprintInfo

router = APIRouter(
    prefix="/blueprints",
    tags=["Blueprints"]
)


@router.post("/", response_model=BlueprintInfo)
async def create_blueprint(
    data: BlueprintCreate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Создание нового чертежа"""
    service = BlueprintsService(session)
    return await service.create(data)


@router.get("/{blueprint_id}", response_model=BlueprintInfo)
async def get_blueprint(
    blueprint_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение чертежа по ID"""
    service = BlueprintsService(session)
    return await service.get_by_id(blueprint_id)


@router.get("/", response_model=List[BlueprintInfo])
async def get_blueprints(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение списка чертежей"""
    service = BlueprintsService(session)
    return await service.get_all(skip, limit)


@router.put("/{blueprint_id}", response_model=BlueprintInfo)
async def update_blueprint(
    blueprint_id: int,
    data: BlueprintUpdate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Обновление чертежа"""
    service = BlueprintsService(session)
    return await service.update(blueprint_id, data)


@router.delete("/{blueprint_id}")
async def delete_blueprint(
    blueprint_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Удаление чертежа"""
    service = BlueprintsService(session)
    await service.delete(blueprint_id)
    return {"message": "Blueprint deleted successfully", "blueprint_id": blueprint_id, "status_code": 200}