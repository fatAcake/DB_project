from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_postgres_db
from services.products_service import ProductsService
from db.sql.schemas.products_schemas import ProductCreate, ProductUpdate, ProductInfo


router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductInfo)
async def create_product(
    data: ProductCreate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Создание нового продукта"""
    service = ProductsService(session)
    return await service.create(data)


@router.get("/{product_id}", response_model=ProductInfo)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение продукта по ID"""
    service = ProductsService(session)
    return await service.get_by_id(product_id)


@router.get("/", response_model=List[ProductInfo])
async def get_products(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение списка продуктов"""
    service = ProductsService(session)
    return await service.get_all(skip, limit)


@router.put("/{product_id}", response_model=ProductInfo)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Обновление продукта"""
    service = ProductsService(session)
    return await service.update(product_id, data)


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Удаление продукта"""
    service = ProductsService(session)
    await service.delete(product_id)
    return {"message": "Product deleted successfully", "product_id": product_id, "status_code": 200}