from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class AdminSettings(Base):
    __tablename__ = "admin_settings"

    id = Column(Integer, primary_key=True, index=True)
    borrow_day_limit = Column(Integer, nullable=True)
    borrow_extend_limit = Column(Integer, nullable=True)
    borrow_book_limit = Column(Integer, nullable=True)
    booking_days_limit = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
