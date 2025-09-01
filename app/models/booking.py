# models/booking.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class BookingStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="bookings")
    
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book = relationship("Book", back_populates="bookings")
    
    booking_date = Column(Date, nullable=False)
    expected_available_date = Column(Date, nullable=False)
    
    status = Column(Enum(BookingStatusEnum), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# models/user.py এ relationship যোগ করতে হবে
# class User(Base):
#     ...
#     bookings = relationship("Booking", back_populates="user")

# models/book.py এ relationship যোগ করতে হবে
# class Book(Base):
#     ...
#     bookings = relationship("Booking", back_populates="book")
