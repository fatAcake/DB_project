from typing import Optional, List
from datetime import datetime
from bson import ObjectId, Binary
from motor.motor_asyncio import AsyncIOMotorCollection
from db.nosql.models import ProductImage, ProductImageCreate, Blueprint, BlueprintCreate

class ProductsImagesCRUD:
    """CRUD для изображений продуктов"""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def create(
            self,
            file_data: bytes,
            filename: str,
            product_id_sql: int, 
            content_type: str = "application/octet-stream"
    ) -> ProductImage:
        """Создание изображения"""
        doc = {
            "image": Binary(file_data),
            "filename": filename,
            "content_type": content_type,
            "product_id_sql": product_id_sql,
            "created_at": datetime.utcnow() # TODO поменять на более новый вид вывода даты 
        }
        
        result = await self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return ProductImage(**doc)
    
    async def get(self, image_id: str) -> Optional[ProductImage]:
        """Получение изображения по ID"""
        doc = await self.collection.find_one({"_id": ObjectId(image_id)})
        if not doc:
            return None
        return ProductImage(**doc)
            
    async def get_all(self) -> list:
        """Получение всех документов из коллекции"""
        return [doc async for doc in self.collection.find({})]
    
    async def get_by_product(self, product_id_sql: int) -> List[ProductImage]:
        """Получение всех изображений продукта"""
        cursor = self.collection.find({"product_id_sql": product_id_sql}).sort("created_at", -1)
        images = []
        
        async for doc in cursor:
            images.append(ProductImage(**doc))
        
        return images
    
    async def delete(self, image_id: str) -> bool:
        """Удаление изображения"""
        result = await self.collection.delete_one({"_id": ObjectId(image_id)})
        return result.deleted_count > 0
    
    async def delete_by_product(self, product_id_sql: int) -> int:
        """Удаление всех изображений продукта"""
        result = await self.collection.delete_many({"product_id_sql": product_id_sql})
        return result.deleted_count