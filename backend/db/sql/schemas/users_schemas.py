from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(..., min_length=1, max_length=255, description="Имя")
    last_name: str = Field(..., min_length=1, max_length=255, description="Фамилия")
    father_name: Optional[str] = Field(None, max_length=255, description="Отчество")
    email: Optional[EmailStr] = Field(None, description="Email")
    is_acive: bool = Field(default=True, description="Активен ли пользователь")


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    hash_password: Optional[str] = Field(None, max_length=255, description="Хэш пароля")
    role_id: int = Field(..., description="ID роли")


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    model_config = ConfigDict(from_attributes=True)

    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    father_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    hash_password: Optional[str] = Field(None, max_length=255)
    role_id: Optional[int] = None
    is_acive: Optional[bool] = None


class UserInDBBase(UserBase):
    """Базовая схема пользователя из БД"""
    id: int = Field(..., description="ID пользователя")
    role_id: int = Field(..., description="ID роли")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления")


class UserResponse(UserInDBBase):
    """Схема для ответа API (без пароля)"""
    pass
