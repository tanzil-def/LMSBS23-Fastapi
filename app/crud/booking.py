from sqlalchemy.orm import Session, joinedload
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate
from typing import List, Optional

def create_booking(db: Session, booking_in: BookingCreate, user_id: int):
    db_booking = Booking(**booking_in.dict(exclude={"user_id"}), user_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking(db: Session, booking_id: int) -> Optional[Booking]:
    return db.query(Booking)\
             .options(joinedload(Booking.user), joinedload(Booking.book))\
             .filter(Booking.id == booking_id)\
             .first()

def get_bookings_by_user(db: Session, user_id: int) -> List[Booking]:
    return db.query(Booking)\
             .options(joinedload(Booking.book))\
             .filter(Booking.user_id == user_id)\
             .all()

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
