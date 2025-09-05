from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.borrow import BorrowStatus  # Enum import

# ==========================
# Nested Response DTOs
# ==========================
class UserResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

    class Config:
        orm_mode = True

class BookResponse(BaseModel):
    id: int
    title: str
    author: Optional[str] = None

    class Config:
        orm_mode = True

# ==========================
# Request DTOs
# ==========================
class BorrowCreate(BaseModel):
    user_id: int
    book_id: int
    days: Optional[int] = 14

class BorrowExtend(BaseModel):
    borrow_id: int
    extend_days: Optional[int] = 7

# ==========================
# Response DTOs
# ==========================
class BorrowResponse(BaseModel):
    id: int
    user: UserResponse
    book: BookResponse
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: BorrowStatus
    extension_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# ==========================
# Borrow Stats Response
# ==========================
class BorrowStatsResponse(BaseModel):
    totalBorrows: int
    activeBorrows: int
    returnedBorrows: int
    overdueBorrows: int
