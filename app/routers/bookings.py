from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from app.crud import booking as crud_booking
from app.dependencies import get_current_user, require_admin

router = APIRouter(tags=["Bookings"])

@router.post("/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(request: BookingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_booking.create_booking(db, request, user_id=current_user.id)

@router.get("/user/me", response_model=List[BookingResponse])
def get_my_bookings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_booking.get_bookings_by_user(db, user_id=current_user.id)

@router.put("/update/{id}", response_model=BookingResponse)
def update_booking(id: int, request: BookingUpdate, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    booking = crud_booking.update_booking(db, id, request)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.delete("/delete/{id}", response_model=BookingResponse)
def delete_booking(id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    booking = crud_booking.delete_booking(db, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
