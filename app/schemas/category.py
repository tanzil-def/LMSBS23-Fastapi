from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Request Schemas
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Name of the category, e.g. Fiction")
    description: Optional[str] = Field(None, max_length=500, description="Description of the category")

class CategoryUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Updated name of the category")
    description: Optional[str] = Field(None, max_length=500, description="Updated description of the category")

# Response Schema
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    book_count: int = Field(..., description="Number of books in this category")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
