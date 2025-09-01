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

# Router with clean prefix handled in main.py
router = APIRouter(tags=["Admin Settings"])

# ✅ 1️⃣ Get current admin settings
@router.get("/", response_model=AdminSettingsResponse)
def get_admin_settings(db: Session = Depends(get_db)):
    return crud_settings.get_settings(db)

# ✅ 2️⃣ Update borrow day limit
@router.post("/borrow-day-limit", response_model=AdminSettingsResponse)
def update_borrow_day_limit(request: BorrowDayLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_borrow_day_limit(db, request.borrow_day_limit)

# ✅ 3️⃣ Update borrow extend limit
@router.post("/borrow-extend-limit", response_model=AdminSettingsResponse)
def update_borrow_extend_limit(request: BorrowExtendLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_borrow_extend_limit(db, request.borrow_extend_limit)

# ✅ 4️⃣ Update borrow book limit
@router.post("/borrow-book-limit", response_model=AdminSettingsResponse)
def update_borrow_book_limit(request: BorrowBookLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_borrow_book_limit(db, request.borrow_book_limit)

# ✅ 5️⃣ Update booking days limit
@router.post("/booking-days-limit", response_model=AdminSettingsResponse)
def update_booking_days_limit(request: BookingDaysLimitRequest, db: Session = Depends(get_db)):
    return crud_settings.set_booking_days_limit(db, request.booking_days_limit)
