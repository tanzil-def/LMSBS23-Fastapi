# app/routers/users.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Dict

from app.db.session import get_db
from app.dependencies import get_current_user
from app.schemas.user import UserResponse
from app.models.borrow import Borrow

router = APIRouter(
    prefix="/user-dashboard",
    tags=["User Dashboard"]
)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user=Depends(get_current_user)):
    """
    Get the currently logged-in user's information
    """
    return current_user

@router.get("/statistics", response_model=Dict[str, int])
def statistics(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get borrowing statistics for the current user
    """
    user_id = current_user.id

    total_borrowed_books = db.query(Borrow).filter(Borrow.user_id == user_id).count()
    total_returned_books = db.query(Borrow).filter(Borrow.user_id == user_id, Borrow.status == "returned").count()
    total_overdue_books = db.query(Borrow).filter(
        Borrow.user_id == user_id,
        Borrow.return_date < func.now(),
        Borrow.status != "returned"
    ).count()

    return {
        "total_borrowed_books": total_borrowed_books,
        "total_returned_books": total_returned_books,
        "total_overdue_books": total_overdue_books
    }

@router.get("/borrowed-books")
def borrowed_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get paginated list of currently borrowed books by the user
    """
    user_id = current_user.id
    query = db.query(Borrow).filter(Borrow.user_id == user_id, Borrow.status == "borrowed")
    total = query.count()
    results = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "data": results,
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }
    }
