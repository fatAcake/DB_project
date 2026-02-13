from typing import List
from fastapi import UploadFile, HTTPException
from db.nosql.crud.products_images import ProductsImagesCRUD
from db.nosql.models import ProductImage


class ProductsImagesService:
    """Сервис для изображений продуктов"""
    
    def __init__(self, crud: ProductsImagesCRUD):
        self.crud = crud
    
    async def upload_image(
        self,
        file: UploadFile,
        product_id_sql: int
    ) -> ProductImage:
        """Загрузка изображения"""
        file_data = await file.read()
        if len(file_data) > 16 * 1024 * 1024:
            raise HTTPException(400, "File size exceeds 16MB limit (MongoDB document size limit)")
        
        return await self.crud.create(
            file_data=file_data,
            filename=file.filename or "unknown",
            product_id_sql=product_id_sql,
            content_type=file.content_type or "application/octet-stream"
        )
    
    async def get_image(self, image_id: str) -> ProductImage:
        """Получение изображения"""
        image = await self.crud.get(image_id)
        if not image:
            raise HTTPException(404, "Image not found")
        return image
    
    async def get_all(self) -> List[dict]:
        """Получение всех изображений"""
        return await self.crud.get_all()
    
    async def get_product_images(self, product_id_sql: int) -> List[ProductImage]:
        """Получение всех изображений продукта"""
        return await self.crud.get_by_product(product_id_sql)
    
    async def delete_image(self, image_id: str) -> bool:
        """Удаление изображения"""
        image = await self.crud.get(image_id)
        if not image:
            raise HTTPException(404, "Image not found")
        return await self.crud.delete(image_id)
    
    async def delete_product_images(self, product_id_sql: int) -> int:
        """Удаление всех изображений продукта"""
        return await self.crud.delete_by_product(product_id_sql)