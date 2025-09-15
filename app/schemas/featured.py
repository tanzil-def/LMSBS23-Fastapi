# app/schemas/featured_book.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ------------------ Base Schema ------------------
class FeaturedBookBase(BaseModel):
    book_id: int

# ------------------ Schema for Create ------------------
class FeaturedBookCreate(FeaturedBookBase):
    pass  # শুধু book_id লাগে create করার সময়

# ------------------ Schema for Update ------------------
class FeaturedBookUpdate(BaseModel):
    book_id: Optional[int] = None

# ------------------ Schema for Response ------------------
class FeaturedBookResponse(BaseModel):
    id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    # nested book info (optional)
    title: Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[int] = None
    cover: Optional[str] = None

    class Config:
        orm_mode = True
