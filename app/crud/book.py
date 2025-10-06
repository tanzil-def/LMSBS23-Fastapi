from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.book import Book

MEDIA_URL = "http://127.0.0.1:8000/media"


def format_book_urls(book: Book) -> Book:
    """
    Add full URLs for cover, pdf_file, and audio_file if they are filenames.
    If the field already has a URL (starts with http), leave it as is.
    """
    if book.cover and not book.cover.startswith("http"):
        book.cover = f"{MEDIA_URL}/cover/{book.cover}"
    if book.pdf_file and not book.pdf_file.startswith("http"):
        book.pdf_file = f"{MEDIA_URL}/pdf/{book.pdf_file}"
    if book.audio_file and not book.audio_file.startswith("http"):
        book.audio_file = f"{MEDIA_URL}/audio/{book.audio_file}"
    return book


# ------------------------------
# CRUD Operations
# ------------------------------

def get_all_books(db: Session):
    books = db.query(Book).all()
    return [format_book_urls(book) for book in books]


def get_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    return format_book_urls(book) if book else None


def is_book_available(db: Session, book_id: int):
    book = get_book(db, book_id)
    return book and book.copies_available > 0


def create_book(db: Session, book_in: dict):
    """
    Create book with file names or URLs. Both uploaded files and URLs work.
    """
    db_book = Book(**book_in)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return format_book_urls(db_book)


def update_book(db: Session, book_id: int, book_in: dict):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    for field, value in book_in.items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return format_book_urls(db_book)


def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    try:
        db.delete(db_book)
        db.commit()
        return {"message": f"Book with id {book_id} deleted successfully."}
    except Exception as e:
        db.rollback()
        raise e


def get_books_by_category(db: Session, category_id: int):
    books = db.query(Book).filter(Book.category_id == category_id).all()
    return [format_book_urls(book) for book in books]


def get_recommended_books(db: Session, limit: int = 10):
    books = db.query(Book).order_by(desc(Book.average_rating)).limit(limit).all()
    return [format_book_urls(book) for book in books]


def get_popular_books(db: Session, limit: int = 10):
    books = db.query(Book).order_by(desc(Book.copies_total)).limit(limit).all()
    return [format_book_urls(book) for book in books]


def get_new_collection(db: Session, limit: int = 10):
    books = db.query(Book).order_by(desc(Book.created_at)).limit(limit).all()
    return [format_book_urls(book) for book in books]
