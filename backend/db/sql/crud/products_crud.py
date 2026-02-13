from datetime import datetime
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from db.sql.models import Products
from db.sql.schemas.products_schemas import ProductCreate, ProductUpdate


async def create_product(session: AsyncSession, data: ProductCreate) -> Products | None:
    """Создание продукта"""
    try:
        product = Products(**data.model_dump())
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка создания продукта",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def get_product(session: AsyncSession, product_id: int) -> Products | None:
    """Получение продукта по ID"""
    try:
        result = await session.execute(
            select(Products).where(Products.id == product_id)
        )
        product = result.scalar_one_or_none()
        return product
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения продукта",
            "product_id": product_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def get_products(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Products] | None:
    """Получение списка продуктов"""
    try:
        result = await session.execute(
            select(Products)
            .offset(skip)
            .limit(limit)
        )
        products = result.scalars().all()
        return list(products)
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения списка продуктов",
            "skip": skip,
            "limit": limit,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def update_product(session: AsyncSession, product_id: int, data: ProductUpdate) -> Products | None:
    """Обновление продукта"""
    try:
        product = await get_product(session, product_id)
        if not product:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        await session.commit()
        await session.refresh(product)
        return product
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка обновления продукта",
            "product_id": product_id,
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def delete_product(session: AsyncSession, product_id: int) -> bool:
    """Удаление продукта"""
    try:
        result = await session.execute(
            delete(Products).where(Products.id == product_id)
        )
        await session.commit()
        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка удаления продукта",
            "product_id": product_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return False