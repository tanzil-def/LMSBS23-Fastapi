from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class BookFormatEnum(str, enum.Enum):
    HARD_COPY = "HARD_COPY"
    E_BOOK = "E_BOOK"
    AUDIO_BOOK = "AUDIO_BOOK"

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # must exist in DB
    short_details = Column(String(255), nullable=True)
    author = Column(String(120), nullable=False)
    about = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="books")

    format = Column(Enum(BookFormatEnum), nullable=False)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)

    isbn = Column(String(50), unique=True, nullable=True)
    publication_year = Column(Integer, nullable=True)

    book_cover_url = Column(String(255), nullable=True)
    pdf_file_url = Column(String(255), nullable=True)
    audio_file_url = Column(String(255), nullable=True)

    borrows = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="book", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
