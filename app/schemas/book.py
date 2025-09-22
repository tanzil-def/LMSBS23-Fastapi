# app/schemas/book.py
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from enum import Enum

class BookFormatEnum(str, Enum):
    HARD_COPY = "HARD_COPY"
    E_BOOK = "E_BOOK"
    AUDIO_BOOK = "AUDIO_BOOK"

# ---------------- Base (common fields)
class BookBase(BaseModel):
    title: str
    author: str
    category_id:  Optional[int] = 1
    format: BookFormatEnum
    copies_total: int = 1
    copies_available: int = 1
    description: Optional[str] = None
    cover: Optional[str] = None
    pdf_file: Optional[str] = None
    audio_file: Optional[str] = None

# ---------------- Create (Request)
class BookCreate(BookBase):
    pass

# ---------------- Update
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category_id:  Optional[int] = 1
    format: Optional[BookFormatEnum] = None
    copies_total: Optional[int] = None
    copies_available: Optional[int] = None
    description: Optional[str] = None
    cover: Optional[str] = None
    pdf_file: Optional[str] = None
    audio_file: Optional[str] = None

# ---------------- Response (Full)
class BookResponse(BookBase):
    id: int
    average_rating: float = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ---------------- Alias
BookRead = BookResponse
