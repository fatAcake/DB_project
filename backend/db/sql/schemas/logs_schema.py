from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, field_validator

class LogCreate(BaseModel):
    user_id: int
    lead_time: datetime
    system: str
    action: str
    response: str

    @field_validator('lead_time', mode='before')
    @classmethod
    def normalize_lead_time(cls, v: Any) -> datetime:
        if isinstance(v, str):
            # Парсим строку → получаем datetime (может быть aware или naive)
            dt = datetime.fromisoformat(v.replace('Z', '+00:00'))  # Z → +00:00 для совместимости
        elif isinstance(v, datetime):
            dt = v
        else:
            raise ValueError("lead_time должен быть строкой ISO или объектом datetime")

        # Убираем timezone, если он есть
        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)   # или dt.astimezone(None) — тоже работает

        return dt
    
class LogUpdate(BaseModel):
    lead_time: Optional[datetime] = None
    system: Optional[str] = None
    action: Optional[str] = None
    response: Optional[str] = None

    @field_validator('lead_time', mode='before')
    @classmethod
    def normalize_lead_time(cls, v: Any) -> datetime | None:
        if v is None:
            return None

        if isinstance(v, str):
            cleaned = v.replace('Z', '+00:00')
            dt = datetime.fromisoformat(cleaned)
        elif isinstance(v, datetime):
            dt = v
        else:
            raise ValueError("lead_time должен быть строкой ISO 8601 или datetime")

        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt

class LogResponse(BaseModel):
    id: int
    user_id: int
    lead_time: datetime
    system: str
    action: str
    response: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True