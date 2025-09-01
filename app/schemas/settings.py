# app/schemas/settings.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ---------------------------
# Response Schema
# ---------------------------
class AdminSettingsResponse(BaseModel):
    id: int
    borrow_day_limit: Optional[int]
    borrow_extend_limit: Optional[int]
    borrow_book_limit: Optional[int]
    booking_days_limit: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ---------------------------
# Request Schemas for each setting
# ---------------------------
class BorrowDayLimitRequest(BaseModel):
    borrow_day_limit: int = Field(..., gt=0, description="Maximum number of days a user can borrow a book")

class BorrowExtendLimitRequest(BaseModel):
    borrow_extend_limit: int = Field(..., ge=0, description="Maximum number of times a borrow can be extended")

class BorrowBookLimitRequest(BaseModel):
    borrow_book_limit: int = Field(..., gt=0, description="Maximum number of books a user can borrow simultaneously")

class BookingDaysLimitRequest(BaseModel):
    booking_days_limit: int = Field(..., gt=0, description="Maximum number of days a booking can be held")
