from typing import Optional, List
from datetime import datetime
from bson import ObjectId, Binary
from motor.motor_asyncio import AsyncIOMotorCollection
from db.nosql.models import Blueprint  

class BlueprintsCRUD:
    """CRUD для чертежей"""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def create(
        self,
        file_data: bytes,
        filename: str,
        blueprint_id_sql: int,
        content_type: str = "application/octet-stream"
    ) -> Blueprint:
        """Создание чертежа"""
        doc = {
            "image": Binary(file_data),
            "filename": filename,
            "content_type": content_type,
            "blueprint_id_sql": blueprint_id_sql,
            "created_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return Blueprint(**doc)  # ← Blueprint (не Blueprints!)
    
    async def get(self, blueprint_id: str) -> Optional[Blueprint]:
        """Получение чертежа по ID"""
        doc = await self.collection.find_one({"_id": ObjectId(blueprint_id)})
        if not doc:
            return None
        return Blueprint(**doc)
    
    async def get_all(self) -> list:
        """Получение всех чертежей"""
        return [doc async for doc in self.collection.find({})]
    
    async def get_by_blueprint_sql(self, blueprint_id_sql: int) -> List[Blueprint]:
        """Получение всех чертежей для записи"""
        cursor = self.collection.find({"blueprint_id_sql": blueprint_id_sql}).sort("created_at", -1)
        blueprints = []
        
        async for doc in cursor:
            blueprints.append(Blueprint(**doc))
        
        return blueprints
    
    async def delete(self, blueprint_id: str) -> bool:
        """Удаление чертежа"""
        result = await self.collection.delete_one({"_id": ObjectId(blueprint_id)})
        return result.deleted_count > 0
    
    async def delete_by_blueprint_sql(self, blueprint_id_sql: int) -> int:
        """Удаление всех чертежей для записи"""
        result = await self.collection.delete_many({"blueprint_id_sql": blueprint_id_sql})
        return result.deleted_count