from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TransactionBase(BaseModel):
    """Базовая схема транзакции"""
    sum: float = Field(..., gt=0, description="Сумма транзакции")
    card_data: Dict[str, Any] = Field(..., description="Данные карты в формате JSON")
    user_id: int = Field(..., gt=0, description="ID пользователя")


class TransactionCreate(TransactionBase):
    """Схема для создания транзакции"""
    pass


class TransactionUpdate(BaseModel):
    """Схема для обновления транзакции"""
    sum: Optional[float] = Field(None, gt=0)
    card_data: Optional[Dict[str, Any]] = None
    user_id: Optional[int] = Field(None, gt=0)


class TransactionInfo(TransactionBase):
    """Схема для ответа с информацией о транзакции"""
    id: int = Field(..., description="ID транзакции")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления")
    
    class Config:
        from_attributes = True