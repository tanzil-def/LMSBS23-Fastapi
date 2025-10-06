from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from fastapi import Request

class BookFormatEnum(str, Enum):
    HARD_COPY = "HARD_COPY"
    E_BOOK = "E_BOOK"
    AUDIO_BOOK = "AUDIO_BOOK"

class BookBase(BaseModel):
    title: str
    author: str
    category_id: Optional[int] = 1
    format: BookFormatEnum
    copies_total: int = 1
    copies_available: int = 1
    description: Optional[str] = None

    cover: Optional[str] = None
    pdf_file: Optional[str] = None
    audio_file: Optional[str] = None


class BookCreate(BookBase):
    """Router এ UploadFile """
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[int] = 1
    format: Optional[BookFormatEnum] = None
    copies_total: Optional[int] = None
    copies_available: Optional[int] = None
    description: Optional[str] = None

    cover: Optional[str] = None
    pdf_file: Optional[str] = None
    audio_file: Optional[str] = None


class BookResponse(BookBase):
    id: int
    average_rating: float = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @staticmethod
    def as_response(book, request: Request = None):
        data = BookResponse.from_orm(book).dict()
        if request:
            base_url = str(request.base_url).rstrip("/")
            if book.cover and not book.cover.startswith("http"):
                data["cover"] = f"{base_url}/media/covers/{book.cover}"
            if book.pdf_file and not book.pdf_file.startswith("http"):
                data["pdf_file"] = f"{base_url}/media/pdfs/{book.pdf_file}"
            if book.audio_file and not book.audio_file.startswith("http"):
                data["audio_file"] = f"{base_url}/media/audio/{book.audio_file}"
        return data


BookRead = BookResponse
