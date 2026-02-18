from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator

class LogCreate(BaseModel):
    """Защита от инъекций: все строки ограничены по длине, в БД идут через ORM с параметрами."""
    user_id: int
    lead_time: Optional[datetime] = None
    system: str = Field(..., min_length=1, max_length=255)
    action: str = Field(..., min_length=1, max_length=5000)
    response: str = Field(..., min_length=1, max_length=5000)

    @field_validator('lead_time', mode='before')
    @classmethod
    def normalize_lead_time(cls, v: Any) -> Optional[datetime]:
        if v is None:
            return None
        if isinstance(v, str):
            dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
        elif isinstance(v, datetime):
            dt = v
        else:
            raise ValueError("lead_time должен быть строкой ISO или объектом datetime")
        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt
    
class LogUpdate(BaseModel):
    lead_time: Optional[datetime] = None
    system: Optional[str] = Field(None, min_length=1, max_length=255)
    action: Optional[str] = Field(None, min_length=1, max_length=5000)
    response: Optional[str] = Field(None, min_length=1, max_length=5000)

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