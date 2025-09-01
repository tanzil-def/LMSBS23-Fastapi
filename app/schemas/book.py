from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from enum import Enum

# -------------------
class BookFormatEnum(str, Enum):
    HARD_COPY = "HARD_COPY"
    E_BOOK = "E_BOOK"
    AUDIO_BOOK = "AUDIO_BOOK"

# ------------------- Base schema (common fields)
class BookBase(BaseModel):
    name: str
    author: str
    category_id: int
    format: BookFormatEnum
    total_copies: int = 1
    available_copies: int = 1
    short_details: Optional[str] = None
    about: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    book_cover_url: Optional[HttpUrl] = None
    pdf_file_url: Optional[HttpUrl] = None
    audio_file_url: Optional[HttpUrl] = None

# ------------------- Request DTOs
class BookCreate(BookBase):
    """Schema for creating a new book"""
    pass

class BookUpdate(BaseModel):
    """Schema for updating an existing book"""
    name: Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[int] = None
    format: Optional[BookFormatEnum] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    short_details: Optional[str] = None
    about: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    book_cover_url: Optional[HttpUrl] = None
    pdf_file_url: Optional[HttpUrl] = None
    audio_file_url: Optional[HttpUrl] = None

# ------------------- Response DTO
class BookResponse(BookBase):
    """Schema for reading book details (response)"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ------------------- Alias for backward compatibility
BookRead = BookResponse
