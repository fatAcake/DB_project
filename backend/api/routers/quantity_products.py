from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_postgres_db
from services.quantity_products_service import QuantityProductsService
from db.sql.schemas.quantity_products_schemas import QuantityProductCreate, QuantityProductUpdate, QuantityProductInfo

router = APIRouter(prefix="/quantity_products", tags=["QuantityProducts"])

@router.post("/", response_model=QuantityProductInfo)
async def create(
    data: QuantityProductCreate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Создание нового количества продукта"""
    service = QuantityProductsService(session)
    return await service.create(data)

@router.get("/{quantity_id}", response_model=QuantityProductInfo)
async def get(
    quantity_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение количества продукта по ID"""
    service = QuantityProductsService(session)
    return await service.get(quantity_id)

@router.get("/", response_model=List[QuantityProductInfo])
async def get_all(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=100, description="Лимит записей"),
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение количетсва продуктов"""
    service = QuantityProductsService(session)
    return await service.get_all(skip, limit)

@router.get("/products/{product_id}", response_model=QuantityProductInfo)
async def get_by_product_id(
    product_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение количества продуктов по Products.id"""
    service = QuantityProductsService(session)
    return await service.get_by_product_id(product_id)

@router.put("/{quantity_id}", response_model=QuantityProductInfo)
async def update(
    quantity_id: int, 
    data: QuantityProductUpdate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Обновление количества продукта по ID"""
    service = QuantityProductsService(session)
    return await service.update(quantity_id, data)

@router.delete("/{quantity_id}")
async def delete(
    quantity_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Удаление количества продукта по ID"""
    service = QuantityProductsService(session)
    await service.delete(quantity_id)
    return {"message": "Quantity product deleted successfully", "quantity_product_id": quantity_id, "status_code": 200}

@router.delete("/products/{product_id}")
async def delete(
    product_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Удаление количества продукта по Products.id"""
    service = QuantityProductsService(session)
    await service.delete_by_product_id(product_id)
    return {"message": "Quantity product by product id deleted successfully", "product_id": product_id, "status_code": 200}