from datetime import datetime
from typing import Optional, Annotated, Any, Union
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator
from pydantic_core import core_schema
from bson import ObjectId, Binary

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.chain_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x), return_schema=core_schema.str_schema()
            ),
        )


class ProductImageBase(BaseModel):
    """Базовая модель без поля image (для ответов)"""
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
    
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    product_id_sql: int
    filename: str
    content_type: str = "application/octet-stream"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProductImage(ProductImageBase):
    """Полная модель с бинарными данными (для внутреннего использования)"""
    image: Union[bytes, Binary] = Field(exclude=True) 
    
    @field_validator('image', mode='before')
    @classmethod
    def validate_image(cls, v):
        """Конвертируем bytes в Binary если нужно"""
        if isinstance(v, bytes):
            return v  # Оставляем как bytes
        elif isinstance(v, Binary):
            return v
        raise ValueError("Image must be bytes or Binary")
    
    @computed_field
    @property
    def image_size(self) -> int:
        """Размер изображения в байтах"""
        return len(self.image) if self.image else 0


class ProductImageCreate(BaseModel):
    """Модель для создания"""
    product_id_sql: int


class ProductImageResponse(ProductImageBase):
    """Модель для ответа API (без бинарных данных)"""
    image_size: int


# === Blueprints ===
class BlueprintBase(BaseModel):
    """Базовая модель без поля image (для ответов)"""
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
    
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    blueprint_id_sql: int
    filename: str
    content_type: str = "application/octet-stream"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Blueprint(BlueprintBase):
    """Полная модель с бинарными данными (для внутреннего использования)"""
    image: Union[bytes, Binary] = Field(exclude=True)  # Принимаем и bytes, и Binary
    
    @field_validator('image', mode='before')
    @classmethod
    def validate_image(cls, v):
        """Конвертируем bytes в Binary если нужно"""
        if isinstance(v, bytes):
            return v
        elif isinstance(v, Binary):
            return v
        raise ValueError("Image must be bytes or Binary")
    
    @computed_field
    @property
    def image_size(self) -> int:
        """Размер чертежа в байтах"""
        return len(self.image) if self.image else 0


class BlueprintCreate(BaseModel):
    """Модель для создания"""
    blueprint_id_sql: int


class BlueprintResponse(BlueprintBase):
    """Модель для ответа API (без бинарных данных)"""
    image_size: int