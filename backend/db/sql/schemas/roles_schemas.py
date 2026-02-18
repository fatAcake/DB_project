from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class RoleBase(BaseModel):
    """Базовая схема роли"""
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=255, description="Название роли")
    description: Optional[str] = Field(None, max_length=255, description="Описание роли")


class RoleCreate(RoleBase):
    """Схема для создания роли"""
    pass


class RoleUpdate(BaseModel):
    """Схема для обновления роли"""
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=255)


class RoleInDBBase(RoleBase):
    """Базовая схема роли из БД"""
    id: int = Field(..., description="ID роли")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления")


class RoleResponse(RoleInDBBase):
    """Схема для ответа API"""
    pass
