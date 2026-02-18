from pydantic import BaseModel, Field
from typing import Optional

class BlueprintBase(BaseModel):
    """Базовая схема чертежа"""
    name: str = Field(..., min_length=1, max_length=200, description="Название чертежа")
    description: Optional[str] = Field(None, max_length=1000, description="Описание чертежа")

class BlueprintCreate(BlueprintBase):
    """Схема для создания чертежа"""
    pass

class BlueprintUpdate(BlueprintBase):
    """Схема для обновления чертежа"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class BlueprintInfo(BlueprintBase):
    """Схема для ответа с информацией о чертеже"""
    id: int = Field(..., description="ID чертежа")
    
    class Config:
        from_attributes = True