from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
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
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    cover = Column(String(255), nullable=True)
    pdf_file = Column(String(255), nullable=True)
    audio_file = Column(String(255), nullable=True)

    copies_total = Column(Integer, nullable=True)
    copies_available = Column(Integer, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="books")

    average_rating = Column(Float, default=0)
    format = Column(Enum(BookFormatEnum), nullable=False)

    borrows = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="book", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
