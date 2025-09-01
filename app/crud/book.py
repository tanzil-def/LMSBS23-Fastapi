from sqlalchemy.orm import Session, selectinload
from app.models.book import Book
from app.schemas.book import BookCreate

def get_all_books(db: Session):
    return db.query(Book).options(
        selectinload(Book.category),
        selectinload(Book.bookings)
    ).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).options(
        selectinload(Book.category),
        selectinload(Book.bookings)
    ).filter(Book.id == book_id).first()

def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: BookCreate):
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        return None
    for key, value in book.dict().items():
        setattr(existing_book, key, value)
    db.commit()
    db.refresh(existing_book)
    return existing_book

def delete_book(db: Session, book_id: int):
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        return False
    db.delete(existing_book)
    db.commit()
    return True
