from pydantic import BaseModel, Field
from typing import Optional


class ConfirmPassportDataBase(BaseModel):
    """Базовая схема подтверждения паспортных данных"""
    passport_data_id: int = Field(..., gt=0, description="ID паспортных данных")
    is_confirm: bool = Field(..., description="Статус подтверждения")


class ConfirmPassportDataCreate(ConfirmPassportDataBase):
    """Схема для создания подтверждения паспортных данных"""
    pass


class ConfirmPassportDataUpdate(BaseModel):
    """Схема для обновления подтверждения паспортных данных"""
    passport_data_id: Optional[int] = Field(None, gt=0)
    is_confirm: Optional[bool] = None


class ConfirmPassportDataInfo(ConfirmPassportDataBase):
    """Схема для ответа с информацией о подтверждении паспортных данных"""
    id: int = Field(..., description="ID подтверждения")
    
    class Config:
        from_attributes = True