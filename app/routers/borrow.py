from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.crud import borrow as borrow_crud
from app.schemas import borrow as borrow_schema

router = APIRouter(prefix="/api/borrow", tags=["Borrow & Return"])

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

@router.get("/user/{user_id}", response_model=List[borrow_schema.BorrowResponse])
def get_user_borrows(user_id: int = Path(...), db: Session = Depends(get_db)):
    return borrow_crud.get_user_borrows(db, user_id)

@router.get("/overdue", response_model=List[borrow_schema.BorrowResponse])
def get_overdue_borrows(db: Session = Depends(get_db)):
    return borrow_crud.get_overdue_borrows(db)

@router.get("/stats")
def get_borrow_stats(db: Session = Depends(get_db)):
    return borrow_crud.get_borrow_stats(db)
