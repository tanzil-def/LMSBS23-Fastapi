from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import requests

from app.db.session import get_db
from app.schemas.book import BookResponse, BookCreate, BookUpdate
from app.crud import book as crud_book
from app.dependencies import require_admin
from app.models.user import User

router = APIRouter(tags=["Book Management📖"])  # No prefix

# ------------------------------
# Public Endpoints
# ------------------------------

@router.get("/list", response_model=List[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return crud_book.get_all_books(db)

@router.get("/{id}/is_available")
def check_availability(id: int, db: Session = Depends(get_db)):
    available = crud_book.is_book_available(db, id)
    if available is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book_id": id, "is_available": available}

@router.get("/search", response_model=List[BookResponse])
def search_books(q: str, db: Session = Depends(get_db)):
    all_books = crud_book.get_all_books(db)
    return [b for b in all_books if q.lower() in b.title.lower() or q.lower() in b.author.lower()]

@router.get("/retrieve/{id}", response_model=BookResponse)
def retrieve_book(id: int, db: Session = Depends(get_db)):
    book = crud_book.get_book(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/recommended-books", response_model=List[BookResponse])
def recommended_books(db: Session = Depends(get_db)):
    return crud_book.get_recommended_books(db)

@router.get("/popular-books", response_model=List[BookResponse])
def popular_books(db: Session = Depends(get_db)):
    return crud_book.get_popular_books(db)

@router.get("/new-collection", response_model=List[BookResponse])
def new_collection(db: Session = Depends(get_db)):
    return crud_book.get_new_collection(db)

@router.get("/category/{categoryId}", response_model=List[BookResponse])
def filter_by_category(categoryId: int, db: Session = Depends(get_db)):
    return crud_book.get_books_by_category(db, categoryId)

@router.get("/available", response_model=List[BookResponse])
def available_books(db: Session = Depends(get_db)):
    all_books = crud_book.get_all_books(db)
    return [b for b in all_books if b.copies_available > 0]

# ------------------------------
# Admin-only Endpoints
# ------------------------------

@router.post("/create", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(request: BookCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    return crud_book.create_book(db, request)

@router.post("/create/with-links", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_with_links(request: BookCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    return crud_book.create_book(db, request)

@router.put("/edit/{id}", response_model=BookResponse)
def edit_book(id: int, request: BookUpdate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    book = crud_book.update_book(db, id, request)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/{id}/availability", response_model=BookResponse)
def update_availability(id: int, copies_available: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    book = crud_book.update_book(db, id, BookUpdate(copies_available=copies_available))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/delete/{id}")
def delete_book_endpoint(id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    result = crud_book.delete_book(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}


