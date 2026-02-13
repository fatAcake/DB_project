from datetime import datetime
from typing import Optional, Any              # ← вот здесь добавь Optional
from pydantic import BaseModel, field_validator

class PassportDataCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    father_name: Optional[str] = None         # теперь будет работать
    birth_date: datetime
    place_birth: str
    number_passport: str
    passport_issue_date: str
    issued_by: str
    code_issued_by: str
    registration: str

    @field_validator('birth_date', mode='before')
    @classmethod
    def normalize_birth_date(cls, v: Any) -> datetime:
        if isinstance(v, str):
            cleaned = v.replace('Z', '+00:00')
            dt = datetime.fromisoformat(cleaned)
        elif isinstance(v, datetime):
            dt = v
        else:
            raise ValueError("birth_date должен быть строкой ISO 8601 или объектом datetime")

        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)

        return dt
    

class PassportDataUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    birth_date: Optional[datetime] = None     # ← здесь Optional[datetime]
    place_birth: Optional[str] = None
    number_passport: Optional[str] = None
    passport_issue_date: Optional[str] = None
    issued_by: Optional[str] = None
    code_issued_by: Optional[str] = None
    registration: Optional[str] = None

    @field_validator('birth_date', mode='before')
    @classmethod
    def normalize_birth_date(cls, v: Any) -> datetime | None:
        if v is None:
            return None

        if isinstance(v, str):
            cleaned = v.replace('Z', '+00:00')
            dt = datetime.fromisoformat(cleaned)
        elif isinstance(v, datetime):
            dt = v
        else:
            raise ValueError("birth_date должен быть строкой ISO 8601 или объектом datetime")

        # Приводим к naive
        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)

        return dt

class PassportDataResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    father_name: Optional[str] = None
    birth_date: datetime
    place_birth: str
    number_passport: str
    passport_issue_date: str
    issued_by: str
    code_issued_by: str
    registration: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True