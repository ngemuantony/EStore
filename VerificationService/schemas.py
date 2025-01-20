from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class VerificationBase(BaseModel):
    user_id: int
    email: EmailStr

class VerificationCreate(VerificationBase):
    pass

class Verification(VerificationBase):
    id: int
    code: str
    is_verified: bool
    expires_at: datetime
    created_at: datetime
    verified_at: Optional[datetime]

    class Config:
        orm_mode = True

class VerificationResponse(BaseModel):
    message: str
    verification_link: Optional[str] = None
