from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum
from app.schemas.user import UserResponse
from app.schemas.book import BookRead

class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

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
    booking_date: date
    expected_available_date: Optional[date] = None
    status: BookingStatus
    days_until_available: Optional[int] = None
    can_be_cancelled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

BookingResponse = BookingRead
