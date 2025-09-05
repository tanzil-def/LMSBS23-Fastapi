from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.crud import borrow as borrow_crud
from app.schemas import borrow as borrow_schema

router = APIRouter(tags=["Borrow & Return"])

# ==========================
# Borrow Management (User)
# ==========================

@router.post("/create", response_model=borrow_schema.BorrowResponse)
def create_borrow(request: borrow_schema.BorrowCreate, db: Session = Depends(get_db)):
    borrow = borrow_crud.create_borrow(db, request)
    if not borrow:
        raise HTTPException(status_code=400, detail="Book not available or user limit reached")
    return borrow

@router.put("/return", response_model=borrow_schema.BorrowResponse)
def return_book(user_id: int = Query(...), book_id: int = Query(...), db: Session = Depends(get_db)):
    borrow = borrow_crud.return_book(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Book already returned or borrow not found")
    return borrow

@router.put("/extend_due_date", response_model=borrow_schema.BorrowResponse)
def extend_due_date(
    user_id: int = Query(...),
    book_id: int = Query(...),
    extend_days: Optional[int] = Query(7),
    db: Session = Depends(get_db)
):
    borrow = borrow_crud.extend_due_date(db, user_id, book_id, extend_days)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot extend due date")
    return borrow

# ==========================
# Borrow Info (User/Admin)
# ==========================

@router.get("/user/{user_id}", response_model=List[borrow_schema.BorrowResponse])
def get_user_borrows(user_id: int = Path(...), db: Session = Depends(get_db)):
    return borrow_crud.get_user_borrows(db, user_id)

@router.get("/user/{user_id}/history", response_model=List[borrow_schema.BorrowResponse])
def get_user_borrow_history(user_id: int = Path(...), db: Session = Depends(get_db)):
    return borrow_crud.get_user_borrow_history(db, user_id)

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
def reject_borrow_request(user_id: int = Query(...), book_id: int = Query(...), db: Session = Depends(get_db)):
    borrow = borrow_crud.reject_borrow(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot reject borrow request")
    return borrow

@router.put("/pending", response_model=borrow_schema.BorrowResponse)
def mark_borrow_pending(user_id: int = Query(...), book_id: int = Query(...), db: Session = Depends(get_db)):
    borrow = borrow_crud.mark_pending(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot mark borrow as pending")
    return borrow

@router.put("/activate", response_model=borrow_schema.BorrowResponse)
def activate_borrow_request(user_id: int = Query(...), book_id: int = Query(...), db: Session = Depends(get_db)):
    borrow = borrow_crud.activate_borrow(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot activate borrow request")
    return borrow

@router.put("/accept", response_model=borrow_schema.BorrowResponse)
def accept_borrow_request(user_id: int = Query(...), book_id: int = Query(...), db: Session = Depends(get_db)):
    borrow = borrow_crud.accept_borrow(db, user_id, book_id)
    if not borrow:
        raise HTTPException(status_code=400, detail="Cannot accept borrow request")
    return borrow

# ==========================
# Borrow Statistics (Admin)
# ==========================

@router.get("/stats", response_model=borrow_schema.BorrowStatsResponse)
def get_borrow_stats(db: Session = Depends(get_db)):
    return borrow_crud.get_borrow_stats(db)
