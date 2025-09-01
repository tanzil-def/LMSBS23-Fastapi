from pydantic import BaseModel
from typing import Optional

# Request DTOs
class ReviewCreateRequest(BaseModel):
    userId: int
    rating: int
    comment: Optional[str] = None

class ReviewUpdateRequest(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

# Response DTO
class ReviewResponse(BaseModel):
    id: int
    user: dict
    book: dict
    rating: int
    comment: Optional[str]
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
