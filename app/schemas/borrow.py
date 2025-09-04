from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.borrow import BorrowStatus  # ✅ Model Enum import

# Request DTOs
class BorrowCreate(BaseModel):
    user_id: int
    book_id: int
    days: Optional[int] = 14

class BorrowExtend(BaseModel):
    borrow_id: int
    extend_days: Optional[int] = 7

# Response DTO
class BorrowResponse(BaseModel):
    id: int
    user: dict
    book: dict
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: BorrowStatus  
    extension_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
