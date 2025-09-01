# app/routers/settings.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.settings import (
    AdminSettingsResponse,
    BorrowDayLimitRequest,
    BorrowExtendLimitRequest,
    BorrowBookLimitRequest,
    BookingDaysLimitRequest
)
from app.crud import settings as crud_settings

router = APIRouter(prefix="/api/admin-settings", tags=["Admin Settings"])

@router.get("/", response_model=AdminSettingsResponse)
def get_admin_settings(db: Session = Depends(get_db)):
    return crud_settings.get_settings(db)

@router.post("/borrow-day-limit", response_model=AdminSettingsResponse)
def update_borrow_day_limit(request: BorrowDayLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_borrow_day_limit(db, request.borrow_day_limit)

@router.post("/borrow-extend-limit", response_model=AdminSettingsResponse)
def update_borrow_extend_limit(request: BorrowExtendLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_borrow_extend_limit(db, request.borrow_extend_limit)

@router.post("/borrow-book-limit", response_model=AdminSettingsResponse)
def update_borrow_book_limit(request: BorrowBookLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_borrow_book_limit(db, request.borrow_book_limit)

@router.post("/booking-days-limit", response_model=AdminSettingsResponse)
def update_booking_days_limit(request: BookingDaysLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_booking_days_limit(db, request.booking_days_limit)
