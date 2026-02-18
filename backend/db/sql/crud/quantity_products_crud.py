from datetime import datetime
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from db.sql.models import QuantityProducts
from db.sql.schemas.quantity_products_schemas import QuantityProductCreate, QuantityProductUpdate

logger = logging.getLogger("uvicorn")

async def create_quantity_product(
        session: AsyncSession, 
        data: QuantityProductCreate) -> QuantityProducts | None: 
    try:
        existing = await session.execute(select(QuantityProducts).where(
            QuantityProducts.product_id == data.product_id
        ))
        qp = existing.scalar_one_or_none()

        if qp:
            qp.count+=data.count
        else:
            qp = QuantityProducts(**data.model_dump())
            session.add(qp)

        await session.commit()
        await session.refresh(qp)
        return qp
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка создания 'QuantityProduct'",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def get_quantity_product(
        session: AsyncSession, 
        id: int) -> QuantityProducts:
    try:
        res = await session.execute(select(QuantityProducts).where(
            QuantityProducts.id == id
        ))
        qp = res.scalar_one_or_none()
        return qp
    except Exception as e:
        logger.error(json.dumps({
            "message": "Ошибка получения 'QuantityProduct'",
            "quantity_product_id": id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None
    
async def get_quantity_product_by_product_id(
        session: AsyncSession, 
        product_id: int) -> QuantityProducts:
    try:
        res = await session.execute(select(QuantityProducts).where(
            QuantityProducts.product_id == product_id
        ))
        qp = res.scalar_one_or_none()
        return qp
    except Exception as e:
        logger.error(json.dumps({
            "message": "Ошибка получения 'QuantityProduct' по Products.id",
            "product_id": product_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def get_quantity_products(
        session: AsyncSession,
        skip: int = 0, limit: int = 100) -> list[QuantityProducts]:
    try:
        result = await session.execute(
            select(QuantityProducts)
            .offset(skip)
            .limit(limit)
        )
        qps = result.scalars().all()
        return qps
    except Exception as e:
        logger.error(json.dumps({
            "message": "Ошибка получения 'QuantityProduct's'",
            "skip": skip,
            "limit": limit,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def update_quantity_product(
        session: AsyncSession,
        id: int,
        data: QuantityProductUpdate) -> QuantityProducts:
    try:
        qp = await get_quantity_product(session, id)

        if not qp:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(qp, field, value)

        await session.commit()
        await session.refresh(qp)
        return qp
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка обновления 'QuantityProduct'",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def delete_quantity_product(
        session: AsyncSession,
        id: int) -> bool:
    try:
        res = await session.execute(delete(QuantityProducts).where(
            QuantityProducts.id == id
        ))
        await session.commit()
        return res.rowcount > 0
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка удаления 'QuantityProduct'",
            "quantity_product_id": id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None

async def delete_quantity_product_by_product_id(
        session: AsyncSession,
        product_id: int) -> bool:
    try:
        res = await session.execute(delete(QuantityProducts).where(
            QuantityProducts.product_id == product_id
        ))
        await session.commit()
        return res.rowcount > 0
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка удаления 'QuantityProduct' по Products.id ",
            "quantity_product_id": id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None