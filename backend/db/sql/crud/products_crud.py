from datetime import datetime
from typing import Tuple
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from db.sql.models import Products, QuantityProducts
from db.sql.schemas.products_schemas import ProductCreate, ProductUpdate
from db.sql.crud.quantity_products_crud import create_quantity_product, delete_quantity_product_by_product_id, get_quantity_product_by_product_id, get_quantity_products
from db.sql.schemas.quantity_products_schemas import QuantityProductCreate
logger = logging.getLogger("uvicorn")
async def create_product(session: AsyncSession, data: ProductCreate) -> Products | None:
    """Создание продукта"""
    try:
        product = Products(**data.model_dump())
        session.add(product)

        await session.commit()
        await session.refresh(product)
        await create_quantity_product(
            session, 
            QuantityProductCreate(count=1, product_id=product.id))
        
        return product
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка создания продукта",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def get_product(session: AsyncSession, product_id: int) -> Tuple[Products, QuantityProducts] | None:
    """Получение продукта по ID"""
    try:
        result = await session.execute(
            select(Products).where(Products.id == product_id)
        )
        product = result.scalar_one_or_none()
        qp = await get_quantity_product_by_product_id(session, product_id)
        return product, qp
    except Exception as e:
        logger.error(json.dumps({
            "message": "Ошибка получения продукта",
            "product_id": product_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None, None


async def get_products(
        session: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
) -> Tuple[list[Products], list[QuantityProducts]] | None:
    """Получение списка продуктов"""
    try:
        result = await session.execute(
            select(Products)
            .offset(skip)
            .limit(limit)
        )

        products = result.scalars().all()
        qps = await get_quantity_products(session, skip, limit)
        return list(products), list(qps)
    except Exception as e:
        logger.error(json.dumps({
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
        logger.error(json.dumps({
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
        result = await get_product(session, product_id)
        if not result:
            return False
        await delete_quantity_product_by_product_id(session, product_id)
        await session.delete(result)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка удаления продукта",
            "product_id": product_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return False