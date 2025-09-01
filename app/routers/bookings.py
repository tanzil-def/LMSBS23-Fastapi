# app/routers/bookings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate, BookingStatus
from app.crud import booking as crud_booking

router = APIRouter(prefix="/api/booking", tags=["Bookings"])

@router.post("/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(request: BookingCreate, db: Session = Depends(get_db)):
    return crud_booking.create_booking(db, request)

@router.get("/{id}", response_model=BookingResponse)
def get_booking(id: int, db: Session = Depends(get_db)):
    booking = crud_booking.get_booking(db, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.get("/user/{user_id}", response_model=List[BookingResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    return crud_booking.get_bookings_by_user(db, user_id)

@router.get("/book/{book_id}", response_model=List[BookingResponse])
def get_book_bookings(book_id: int, db: Session = Depends(get_db)):
    return crud_booking.get_bookings_by_book(db, book_id)

@router.get("/status/{status}", response_model=List[BookingResponse])
def get_bookings_by_status(status: BookingStatus, db: Session = Depends(get_db)):
    return crud_booking.get_bookings_by_status(db, status)

@router.get("/expired", response_model=List[BookingResponse])
def get_expired_bookings(db: Session = Depends(get_db)):
    today = date.today()
    return crud_booking.get_expired_bookings(db, today)

@router.put("/update/{id}", response_model=BookingResponse)
def update_booking(id: int, request: BookingUpdate, db: Session = Depends(get_db)):
    booking = crud_booking.update_booking(db, id, request)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.delete("/delete/{id}", response_model=BookingResponse)
def delete_booking(id: int, db: Session = Depends(get_db)):
    booking = crud_booking.delete_booking(db, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
