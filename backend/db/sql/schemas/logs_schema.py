from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class LogCreate(BaseModel):
    user_id: int
    lead_time: datetime
    system: str
    action: str
    response: str

class LogUpdate(BaseModel):
    lead_time: Optional[datetime] = None
    system: Optional[str] = None
    action: Optional[str] = None
    response: Optional[str] = None

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