from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from db.sql.crud.products_crud import (
    create_product, get_product, get_products,
    update_product, delete_product)
from db.sql.schemas.products_schemas import ProductCreate, ProductUpdate, ProductInfo


class ProductsService:
    """Сервис для работы с продуктами"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: ProductCreate) -> ProductInfo:
        """Создание продукта"""
        product = await create_product(self.session, data)
        if not product:
            raise HTTPException(400, "Failed to create product")
        
        return ProductInfo(
            id=product.id,
            description=product.description,
            price=product.price
        )
    
    async def get_by_id(self, product_id: int) -> ProductInfo:
        """Получение продукта по ID"""
        product, qp = await get_product(self.session, product_id)
        if not product:
            raise HTTPException(404, "Product not found")
        
        return ProductInfo(
            id=product.id,
            description=product.description,
            price=product.price,
            count=qp.count
        )
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductInfo]:
        """Получение списка продуктов с количеством"""
        products, qps = await get_products(self.session, skip, limit)
        if not products:
            raise HTTPException(404, "No products found")
        
        quantity_dict = {qp.product_id: qp.count for qp in qps}
        
        return [
            ProductInfo(
                id=product.id,
                description=product.description,
                price=product.price,
                count=str(quantity_dict.get(product.id, None))
            )
            for product in products
        ]
    
    async def update(self, product_id: int, data: ProductUpdate) -> ProductInfo:
        """Обновление продукта"""
        product = await update_product(self.session, product_id, data)
        if not product:
            raise HTTPException(404, "Product not found")
        
        return ProductInfo(
            id=product.id,
            description=product.description,
            price=product.price
        )
    
    async def delete(self, product_id: int) -> bool:
        """Удаление продукта"""
        success = await delete_product(self.session, product_id)
        if not success:
            raise HTTPException(404, "Product not found")
        return True