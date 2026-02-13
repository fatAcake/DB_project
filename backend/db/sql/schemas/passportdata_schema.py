from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PassportDataCreate(BaseModel):
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

class PassportDataUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    place_birth: Optional[str] = None
    number_passport: Optional[str] = None
    passport_issue_date: Optional[str] = None
    issued_by: Optional[str] = None
    code_issued_by: Optional[str] = None
    registration: Optional[str] = None

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