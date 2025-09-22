# app/routers/borrow.py
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.crud import borrow as borrow_crud
from app.schemas import borrow as borrow_schema
from .auth import get_current_user, get_admin_user  # relative import from routers/

from app.models.user import User

router = APIRouter(tags=["Borrow & Return"])

# ==========================
# Borrow Management (User)
# ==========================

@router.post("/create", response_model=borrow_schema.BorrowResponse)
def create_borrow(
    request: borrow_schema.BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrow = borrow_crud.create_borrow(db, request, current_user.id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Book not available or already borrowed")
    return borrow

@router.put("/return", response_model=borrow_schema.BorrowResponse)
def return_book(
    book_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrow = borrow_crud.return_book(db, current_user.id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Book not borrowed or already returned")
    return borrow

@router.put("/extend_due_date", response_model=borrow_schema.BorrowResponse)
def extend_due_date(
    book_id: int = Query(...),
    extend_days: Optional[int] = Query(7),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrow = borrow_crud.extend_due_date(db, current_user.id, book_id, extend_days)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot extend due date")
    return borrow

# ==========================
# Borrow Info (User/Admin)
# ==========================

@router.get("/user/me", response_model=List[borrow_schema.BorrowResponse])
def get_my_borrows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return borrow_crud.get_user_borrows(db, current_user.id)

@router.get("/list", response_model=List[borrow_schema.BorrowResponse])
def get_all_borrows(db: Session = Depends(get_db)):
    return borrow_crud.get_all_borrows(db)

@router.get("/active", response_model=List[borrow_schema.BorrowResponse])
def get_active_borrows(db: Session = Depends(get_db)):
    return borrow_crud.get_active_borrows(db)

@router.get("/retrieve/{id}", response_model=borrow_schema.BorrowResponse)
def retrieve_borrow(id: int = Path(...), db: Session = Depends(get_db)):
    borrow = borrow_crud.get_borrow_by_id(db, id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow

@router.get("/overdue", response_model=List[borrow_schema.BorrowResponse])
def get_overdue_borrows(db: Session = Depends(get_db)):
    return borrow_crud.get_overdue_borrows(db)

# ==========================
# Borrow Request Management (Admin)
# ==========================

@router.put("/reject", response_model=borrow_schema.BorrowResponse)
def reject_borrow_request(
    user_id: int = Query(...),
    book_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)  # only admin
):
    borrow = borrow_crud.reject_borrow(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot reject borrow request")
    return borrow

@router.put("/accept", response_model=borrow_schema.BorrowResponse)
def accept_borrow_request(
    user_id: int = Query(...),
    book_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)  # only admin
):
    borrow = borrow_crud.accept_borrow(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot accept borrow request")
    return borrow

# ==========================
# Borrow Statistics (Admin)
# ==========================

@router.get("/stats", response_model=borrow_schema.BorrowStatsResponse)
def get_borrow_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)  
):
    return borrow_crud.get_borrow_stats(db)

