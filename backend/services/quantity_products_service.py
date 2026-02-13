from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from db.sql.crud.quantity_products_crud import (
    create_quantity_product, get_quantity_product, get_quantity_products,
    update_quantity_product, delete_quantity_product, get_quantity_product_by_product_id, delete_quantity_product_by_product_id)
from db.sql.schemas.quantity_products_schemas import QuantityProductCreate, QuantityProductUpdate, QuantityProductInfo

class QuantityProductsService:
    """Сервис для работы с количеством продуктов"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: QuantityProductCreate) -> QuantityProductInfo:
        """Создание количества продукта"""
        qp = await create_quantity_product(self.session, data)
        if not qp:
            raise HTTPException(400, "Failed to create quantity product")
        
        return QuantityProductInfo(
            id=qp.id,
            product_id=qp.product_id,
            count=qp.count
        )
    
    async def get(self, id: int) -> QuantityProductInfo:
        """Получение количества продукта по ID"""
        qp = await get_quantity_product(self.session, id)
        if not qp:
            raise HTTPException(404, "Quantity product not found")

        return QuantityProductInfo(
            id=qp.id,
            product_id=qp.product_id,
            count=qp.count
        )
    
    async def get_by_product_id(self, product_id: int) -> QuantityProductInfo:
        """Получение количества продукта по ID"""
        qp = await get_quantity_product_by_product_id(self.session, product_id)
        if not qp:
            raise HTTPException(404, "Quantity product not found")

        return QuantityProductInfo(
            id=qp.id,
            product_id=qp.product_id,
            count=qp.count
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[QuantityProductInfo]:
        """Получение количества продуктов по ID"""
        qps = await get_quantity_products(self.session, skip, limit)
        if not qps:
            raise HTTPException(404, "Quantity product not found")
        
        return [QuantityProductInfo(
            id=qp.id,
            product_id=qp.product_id,
            count=qp.count
        ) for qp in qps]

    async def update(self, id: int, data: QuantityProductUpdate) -> QuantityProductInfo:
        """Обновление количества продукта по ID"""
        qp = await update_quantity_product(self.session, id, data)
        if not qp:
            raise HTTPException(404, "Quantity product not found")
        
        return QuantityProductInfo(
            id=qp.id,
            product_id=qp.product_id,
            count=qp.count
        )
    
    async def delete(self, id: int) -> bool:
        """Удаление количества продукта по ID"""
        success = await delete_quantity_product(self.session, id)
        if not success:
            raise HTTPException(404, "Quantity product not found")
        
        return True
    
    async def delete_by_product_id(self, product_id: int) -> bool:
        """Удаление количества продукта по ID"""
        success = await delete_quantity_product_by_product_id(self.session, product_id)
        if not success:
            raise HTTPException(404, "Quantity product not found")
        
        return True