from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    """Базовая схема продукта"""
    description: str = Field(..., min_length=1, max_length=500, description="Описание продукта")
    price: float = Field(..., gt=0, description="Цена продукта")


class ProductCreate(ProductBase):
    """Схема для создания продукта"""
    pass


class ProductUpdate(ProductBase):
    """Схема для обновления продукта"""
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    price: Optional[float] = Field(None, gt=0)


class ProductInfo(ProductBase):
    """Схема для ответа с информацией о продукте"""
    id: int = Field(..., description="ID продукта")
    
    class Config:
        from_attributes = True  