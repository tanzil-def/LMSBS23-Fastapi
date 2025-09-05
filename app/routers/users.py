from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Dict
from app.db.session import get_db
from app.models.user import User
from app.models.borrow import Borrow, BorrowStatus
from app.schemas.user import UserResponse
from app.dependencies import get_current_user

# -----------------------------
# User Management router
# -----------------------------
router = APIRouter(
    prefix="/api/users",
    tags=["User Management👥"]
)

@router.get("/", response_model=List[UserResponse], summary="Get all users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{id}", response_model=UserResponse, summary="Get user by ID")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{id}/statistics", response_model=Dict[str, int], summary="Get user statistics")
def get_user_statistics(id: int, db: Session = Depends(get_db)):
    total_borrowed = db.query(Borrow).filter(Borrow.user_id == id).count()
    total_returned = db.query(Borrow).filter(
        Borrow.user_id == id,
        Borrow.status == BorrowStatus.RETURNED
    ).count()
    total_overdue = db.query(Borrow).filter(
        Borrow.user_id == id,
        Borrow.return_date < func.now(),
        Borrow.status != BorrowStatus.RETURNED
    ).count()
    return {
        "total_borrowed_books": total_borrowed,
        "total_returned_books": total_returned,
        "total_overdue_books": total_overdue
    }

@router.get("/with-overdue", response_model=List[UserResponse], summary="Get users with overdue books")
def get_users_with_overdue(db: Session = Depends(get_db)):
    subquery = db.query(Borrow.user_id).filter(
        Borrow.return_date < func.now(),
        Borrow.status != BorrowStatus.RETURNED
    ).distinct()
    return db.query(User).filter(User.id.in_(subquery)).all()

@router.get("/search", response_model=List[UserResponse], summary="Search users")
def search_users(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return db.query(User).filter(User.name.ilike(f"%{q}%")).all()

@router.get("/active-borrowers", response_model=List[UserResponse], summary="Get active borrowers")
def get_active_borrowers(db: Session = Depends(get_db)):
    subquery = db.query(Borrow.user_id).filter(Borrow.status == BorrowStatus.ACTIVE).distinct()
    return db.query(User).filter(User.id.in_(subquery)).all()

# -----------------------------
# Dashboard router (separate prefix)
# -----------------------------
dashboard_router = APIRouter(
    prefix="/api/deshbord", 
    tags=["User Dashboard"]
)

@dashboard_router.get("/me", response_model=UserResponse, summary="Get current user info")
def get_current_user_info(current_user=Depends(get_current_user)):
    return current_user

@dashboard_router.get("/statistics", response_model=Dict[str, int], summary="Get current user statistics")
def statistics(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user.id
    total_borrowed_books = db.query(Borrow).filter(Borrow.user_id == user_id).count()
    total_returned_books = db.query(Borrow).filter(
        Borrow.user_id == user_id,
        Borrow.status == BorrowStatus.RETURNED
    ).count()
    total_overdue_books = db.query(Borrow).filter(
        Borrow.user_id == user_id,
        Borrow.return_date < func.now(),
        Borrow.status != BorrowStatus.RETURNED
    ).count()
    return {
        "total_borrowed_books": total_borrowed_books,
        "total_returned_books": total_returned_books,
        "total_overdue_books": total_overdue_books
    }

@dashboard_router.get("/borrowed-books", summary="Get borrowed books with pagination")
def borrowed_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.id
    query = db.query(Borrow).filter(Borrow.user_id == user_id, Borrow.status == BorrowStatus.ACTIVE)
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

