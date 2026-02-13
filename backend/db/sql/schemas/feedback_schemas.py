from pydantic import BaseModel, Field
from typing import Optional


class FeedbackBase(BaseModel):
    """Базовая схема обратной связи"""
    message: str = Field(..., min_length=1, max_length=2000, description="Сообщение обратной связи")
    user_id: int = Field(..., gt=0, description="ID пользователя")


class FeedbackCreate(FeedbackBase):
    """Схема для создания обратной связи"""
    pass


class FeedbackUpdate(BaseModel):
    """Схема для обновления обратной связи"""
    message: Optional[str] = Field(None, min_length=1, max_length=2000)
    user_id: Optional[int] = Field(None, gt=0)


class FeedbackInfo(FeedbackBase):
    """Схема для ответа с информацией об обратной связи"""
    id: int = Field(..., description="ID обратной связи")
    
    class Config:
        from_attributes = True