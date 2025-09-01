from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class DonationStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    name: str

    class Config:
        orm_mode = True

# Request Schemas
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
    status: str
    admin_notes: Optional[str] = None

# Response Schema
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
