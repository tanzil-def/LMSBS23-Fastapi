from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum
from app.schemas.user import UserResponse
from app.schemas.book import BookRead

# Match with DB Enum (IMPORTANT)
class BookingStatus(str, Enum):
    PENDING = "PENDING"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class BookingCreate(BaseModel):
    book_id: int
    expected_available_date: Optional[date] = None

class BookingUpdate(BaseModel):
    expected_available_date: Optional[date] = None
    status: Optional[BookingStatus] = None

class BookingRead(BaseModel):
    id: int
    user: UserResponse
    book: BookRead
    booking_date: Optional[date] = None
    expected_available_date: Optional[date] = None
    status: Optional[BookingStatus] = None
    days_until_available: Optional[int] = None
    can_be_cancelled: Optional[bool] = None   # keep optional, will calculate in service layer
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

BookingResponse = BookingRead
