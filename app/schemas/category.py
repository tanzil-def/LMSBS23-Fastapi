from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    book_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
