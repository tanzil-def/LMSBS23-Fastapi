from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class BorrowStatusEnum(str, Enum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    ACTIVE = "ACTIVE"
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"
    REJECTED = "REJECTED"

# Request DTOs
class BorrowCreate(BaseModel):
    user_id: int
    book_id: int
    days: Optional[int] = 14  # default borrow period

class BorrowReturn(BaseModel):
    borrow_id: int
    return_date: Optional[datetime] = None

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
    status: BorrowStatusEnum
    extension_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
