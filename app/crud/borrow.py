from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from app.models import borrow as borrow_model
from app.schemas import borrow as borrow_schema

# ==========================
# Borrow Management CRUD
# ==========================
def create_borrow(db: Session, request: borrow_schema.BorrowCreate):
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
        status=borrow_model.BorrowStatus.REQUESTED,
        extension_count=0
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(borrow_model.Borrow.id == borrow.id)\
             .first()

def return_book(db: Session, user_id: int, book_id: int):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if not borrow:
        return None
    borrow.return_date = datetime.utcnow()
    borrow.status = borrow_model.BorrowStatus.RETURNED
    db.commit()
    db.refresh(borrow)
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(borrow_model.Borrow.id == borrow.id)\
             .first()

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
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(borrow_model.Borrow.id == borrow.id)\
             .first()

def get_user_borrows(db: Session, user_id: int):
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(borrow_model.Borrow.user_id == user_id)\
             .all()

def get_user_borrow_history(db: Session, user_id: int):
    return get_user_borrows(db, user_id)  # Same query, can add filters if needed

def get_all_borrows(db: Session):
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .all()

def get_active_borrows(db: Session):
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(
                 borrow_model.Borrow.return_date.is_(None),
                 borrow_model.Borrow.status == borrow_model.BorrowStatus.ACTIVE
             ).all()

def get_borrow_by_id(db: Session, borrow_id: int):
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(borrow_model.Borrow.id == borrow_id)\
             .first()

def get_overdue_borrows(db: Session):
    today = datetime.utcnow()
    return db.query(borrow_model.Borrow)\
             .options(joinedload(borrow_model.Borrow.user),
                      joinedload(borrow_model.Borrow.book))\
             .filter(
                 borrow_model.Borrow.return_date.is_(None),
                 borrow_model.Borrow.due_date < today
             ).all()

# ==========================
# Borrow Status Management (Admin)
# ==========================
def reject_borrow(db: Session, user_id: int, book_id: int):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id,
        borrow_model.Borrow.return_date.is_(None)
    ).first()
    if not borrow:
        return None
    borrow.status = borrow_model.BorrowStatus.REJECTED
    db.commit()
    db.refresh(borrow)
    return get_borrow_by_id(db, borrow.id)

def mark_pending(db: Session, user_id: int, book_id: int):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id
    ).first()
    if not borrow:
        return None
    borrow.status = borrow_model.BorrowStatus.PENDING
    db.commit()
    db.refresh(borrow)
    return get_borrow_by_id(db, borrow.id)

def activate_borrow(db: Session, user_id: int, book_id: int):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id
    ).first()
    if not borrow:
        return None
    borrow.status = borrow_model.BorrowStatus.ACTIVE
    db.commit()
    db.refresh(borrow)
    return get_borrow_by_id(db, borrow.id)

def accept_borrow(db: Session, user_id: int, book_id: int):
    borrow = db.query(borrow_model.Borrow).filter(
        borrow_model.Borrow.user_id == user_id,
        borrow_model.Borrow.book_id == book_id
    ).first()
    if not borrow:
        return None
    borrow.status = borrow_model.BorrowStatus.ACCEPTED
    db.commit()
    db.refresh(borrow)
    return get_borrow_by_id(db, borrow.id)

# ==========================
# Borrow Statistics
# ==========================
def get_borrow_stats(db: Session):
    from sqlalchemy import func
    total = db.query(func.count(borrow_model.Borrow.id)).scalar()
    active = db.query(func.count(borrow_model.Borrow.id)).filter(
        borrow_model.Borrow.status == borrow_model.BorrowStatus.ACTIVE
    ).scalar()
    returned = db.query(func.count(borrow_model.Borrow.id)).filter(
        borrow_model.Borrow.status == borrow_model.BorrowStatus.RETURNED
    ).scalar()
    overdue = db.query(func.count(borrow_model.Borrow.id)).filter(
        borrow_model.Borrow.return_date.is_(None),
        borrow_model.Borrow.due_date < datetime.utcnow()
    ).scalar()
    return {
        "totalBorrows": total,
        "activeBorrows": active,
        "returnedBorrows": returned,
        "overdueBorrows": overdue
    }
