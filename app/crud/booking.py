from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from app.models.booking import Booking, BookingStatusEnum as BookingStatus
from app.schemas.booking import BookingCreate, BookingUpdate

def create_booking(db: Session, booking_in: BookingCreate, user_id: int):
    db_booking = Booking(**booking_in.dict(exclude={"user_id"}), user_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking(db: Session, booking_id: int) -> Optional[Booking]:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings_by_user(db: Session, user_id: int) -> List[Booking]:
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def get_bookings_by_book(db: Session, book_id: int) -> List[Booking]:
    return db.query(Booking).filter(Booking.book_id == book_id).all()

def get_bookings_by_status(db: Session, status: BookingStatus) -> List[Booking]:
    return db.query(Booking).filter(Booking.status == status).all()

def get_expired_bookings(db: Session, today: date):
    return db.query(Booking).filter(
        Booking.status == BookingStatus.PENDING,
        Booking.expected_available_date < today
    ).all()

def update_booking(db: Session, booking_id: int, booking_in: BookingUpdate):
    booking = get_booking(db, booking_id)
    if not booking:
        return None
    for field, value in booking_in.dict(exclude_unset=True).items():
        setattr(booking, field, value)
    db.commit()
    db.refresh(booking)
    return booking

def delete_booking(db: Session, booking_id: int):
    booking = get_booking(db, booking_id)
    if not booking:
        return None
    db.delete(booking)
    db.commit()
    return booking
