from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class DonationStatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str  # ✅ Ensure this field is always returned

    class Config:
        orm_mode = True

class DonationCreate(BaseModel):
    user_id: int
    book_title: str
    author: str
    isbn: Optional[str] = None
    notes: Optional[str] = None

class DonationUpdate(BaseModel):
    book_title: str
    author: str
    isbn: Optional[str] = None
    notes: Optional[str] = None

class DonationStatusUpdate(BaseModel):
    status: DonationStatusEnum
    admin_notes: Optional[str] = None

class DonationResponse(BaseModel):
    id: int
    user: UserResponse
    book_title: str
    author: str
    isbn: Optional[str] = None
    notes: Optional[str] = None
    status: DonationStatusEnum
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
