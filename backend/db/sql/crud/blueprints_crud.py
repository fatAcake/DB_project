from datetime import datetime
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from db.sql.models import Blueprints  # Создайте эту модель
from db.sql.schemas.blueprints_schemas import BlueprintCreate, BlueprintUpdate

async def create_blueprint(session: AsyncSession, data: BlueprintCreate) -> Blueprints | None:
    """Создание чертежа"""
    try:
        blueprint = Blueprints(**data.model_dump())
        session.add(blueprint)
        await session.commit()
        await session.refresh(blueprint)
        return blueprint
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка создания чертежа",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def get_blueprint(session: AsyncSession, blueprint_id: int) -> Blueprints | None:
    """Получение чертежа по ID"""
    try:
        result = await session.execute(
            select(Blueprints).where(Blueprints.id == blueprint_id)
        )
        blueprint = result.scalar_one_or_none()
        return blueprint
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения чертежа",
            "blueprint_id": blueprint_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def get_blueprints(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Blueprints] | None:
    """Получение списка чертежей"""
    try:
        result = await session.execute(
            select(Blueprints)
            .offset(skip)
            .limit(limit)
        )
        blueprints = result.scalars().all()
        return list(blueprints)
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения списка чертежей",
            "skip": skip,
            "limit": limit,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def update_blueprint(session: AsyncSession, blueprint_id: int, data: BlueprintUpdate) -> Blueprints | None:
    """Обновление чертежа"""
    try:
        # Получаем чертеж
        blueprint = await get_blueprint(session, blueprint_id)
        if not blueprint:
            return None
        
        # Обновляем поля
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(blueprint, field, value)
        
        await session.commit()
        await session.refresh(blueprint)
        return blueprint
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка обновления чертежа",
            "blueprint_id": blueprint_id,
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def delete_blueprint(session: AsyncSession, blueprint_id: int) -> bool:
    """Удаление чертежа"""
    try:
        result = await session.execute(
            delete(Blueprints).where(Blueprints.id == blueprint_id)
        )
        await session.commit()
        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка удаления чертежа",
            "blueprint_id": blueprint_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return False