# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.book import BookResponse, BookCreate, BookUpdate
from app.crud import book as crud_book

router = APIRouter(tags=["Books"])

@router.get("/list", response_model=List[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return crud_book.get_all_books(db)

@router.get("/{id}/is-available")
def check_availability(id: int, db: Session = Depends(get_db)):
    available = crud_book.is_book_available(db, id)
    if available is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book_id": id, "is_available": available}

@router.post("/create", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(request: BookCreate, db: Session = Depends(get_db)):
    return crud_book.create_book(db, request)

@router.post("/create/with-links", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_with_links(request: BookCreate, db: Session = Depends(get_db)):
    # Later extend korar jonne placeholder
    return crud_book.create_book(db, request)

@router.put("/edit/{id}", response_model=BookResponse)
def edit_book(id: int, request: BookUpdate, db: Session = Depends(get_db)):
    book = crud_book.update_book(db, id, request)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/delete/{id}", response_model=BookResponse)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = crud_book.delete_book(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/category/{categoryId}", response_model=List[BookResponse])
def filter_by_category(categoryId: int, db: Session = Depends(get_db)):
    return crud_book.get_books_by_category(db, categoryId)

@router.get("/recommended", response_model=List[BookResponse])
def recommended_books(db: Session = Depends(get_db)):
    return crud_book.get_recommended_books(db)

@router.get("/popular", response_model=List[BookResponse])
def popular_books(db: Session = Depends(get_db)):
    return crud_book.get_popular_books(db)

@router.get("/new-collection", response_model=List[BookResponse])
def new_collection(db: Session = Depends(get_db)):
    return crud_book.get_new_collection(db)
