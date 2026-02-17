from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    first_name: str = Field(..., min_length=1, description="Имя пользователя")
    last_name: str = Field(..., min_length=1, description="Фамилия пользователя")
    father_name: Optional[str] = Field(None, description="Отчество пользователя")
    email: Optional[str] = Field(None, description="Электронная почта")
    is_acive: bool = Field(True, description="Статус активности")  
    role_id: int = Field(..., gt=0, description="ID роли")


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    hash_password: str = Field(..., description="Хэш пароля")


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    father_name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    hash_password: Optional[str] = Field(None)
    is_acive: Optional[bool] = Field(None)
    role_id: Optional[int] = Field(None, gt=0)


class UserInfo(UserBase):
    """Схема для ответа с информацией о пользователе"""
    id: int = Field(..., description="ID пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления")
    
    
    class Config:
        from_attributes = True