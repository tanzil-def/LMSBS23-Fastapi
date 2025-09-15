# app/models/featured_book.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.book import Book

class FeaturedBook(Base):
    __tablename__ = "featured_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    # relationship pointing to Book
    book = relationship("Book", back_populates="featured_entry", uselist=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
Book.featured_entry = relationship("FeaturedBook", back_populates="book", uselist=False)
