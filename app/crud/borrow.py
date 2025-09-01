from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models import borrow as borrow_model
from app.schemas import borrow as borrow_schema


def create_borrow(db: Session, request: borrow_schema.BorrowCreate):
    # Check if user already borrowed this book and not returned yet
    active = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == request.user_id,
        borrow_model.Borrow.book_id == request.book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if active:
        return None

    borrow = borrow_model.Borrow(
        user_id=request.user_id,
        book_id=request.book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=request.days or 14),
        status="BORROWED",
        extension_count=0
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


def return_book(db: Session, user_id: int, book_id: int):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if not borrow:
        return None

    borrow.return_date = datetime.utcnow()
    borrow.status = "RETURNED"
    db.commit()
    db.refresh(borrow)
    return borrow


def extend_due_date(db: Session, user_id: int, book_id: int, extend_days: int = 7):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if not borrow:
        return None

    borrow.due_date += timedelta(days=extend_days)
    borrow.extension_count += 1
    db.commit()
    db.refresh(borrow)
    return borrow


def get_user_borrows(db: Session, user_id: int):
    return db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id
    ).all()


def get_overdue_borrows(db: Session):
    today = datetime.utcnow()
    return db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.return_date.is_(None),
        borrow_model.Borrow.due_date < today
    ).all()


def get_borrow_stats(db: Session):
    total = db.query(func.count(borrow_model.Borrow.id)).scalar()
    borrowed = db.query(func.count(borrow_model.Borrow.id)).filter(
        borrow_model.Borrow.status == "BORROWED"
    ).scalar()
    returned = db.query(func.count(borrow_model.Borrow.id)).filter(
        borrow_model.Borrow.status == "RETURNED"
    ).scalar()
    overdue = db.query(func.count(borrow_model.Borrow.id)).filter(
        borrow_model.Borrow.return_date.is_(None),
        borrow_model.Borrow.due_date < datetime.utcnow()
    ).scalar()

    return {
        "totalBorrowed": total,
        "borrowedBooks": borrowed,
        "returnedBooks": returned,
        "overdueBooks": overdue
    }
