# app/routers/featured.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.featured import FeaturedBookCreate, FeaturedBookUpdate, FeaturedBookResponse
from app.crud.featured import (
    create_featured_book,
    get_featured_book,
    get_featured_books,
    update_featured_book,
    delete_featured_book
)

router = APIRouter(tags=["Featured Books"], prefix="/api/featured")

# ---------- CREATE ----------
@router.post("/", response_model=FeaturedBookResponse)
def create_featured(featured_in: FeaturedBookCreate, db: Session = Depends(get_db)):
    db_obj = create_featured_book(db=db, obj_in=featured_in)
    return FeaturedBookResponse(
        id=db_obj.id,
        book_id=db_obj.book_id,
        created_at=db_obj.created_at,
        updated_at=db_obj.updated_at,
        title=db_obj.book.title if db_obj.book else None,
        author=db_obj.book.author if db_obj.book else None,
        category_id=db_obj.book.category_id if db_obj.book else None,
        cover=db_obj.book.cover if db_obj.book else None,
    )

# ---------- READ SINGLE ----------
@router.get("/{featured_id}", response_model=FeaturedBookResponse)
def read_featured(featured_id: int, db: Session = Depends(get_db)):
    db_obj = get_featured_book(db=db, featured_id=featured_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Featured book not found")
    return FeaturedBookResponse(
        id=db_obj.id,
        book_id=db_obj.book_id,
        created_at=db_obj.created_at,
        updated_at=db_obj.updated_at,
        title=db_obj.book.title if db_obj.book else None,
        author=db_obj.book.author if db_obj.book else None,
        category_id=db_obj.book.category_id if db_obj.book else None,
        cover=db_obj.book.cover if db_obj.book else None,
    )

# ---------- READ ALL ----------
@router.get("/", response_model=List[FeaturedBookResponse])
def read_featured_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = get_featured_books(db=db, skip=skip, limit=limit)
    return [
        FeaturedBookResponse(
            id=f.id,
            book_id=f.book_id,
            created_at=f.created_at,
            updated_at=f.updated_at,
            title=f.book.title if f.book else None,
            author=f.book.author if f.book else None,
            category_id=f.book.category_id if f.book else None,
            cover=f.book.cover if f.book else None,
        )
        for f in objs
    ]

# ---------- UPDATE ----------
@router.put("/{featured_id}", response_model=FeaturedBookResponse)
def update_featured(featured_id: int, featured_in: FeaturedBookUpdate, db: Session = Depends(get_db)):
    db_obj = get_featured_book(db=db, featured_id=featured_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Featured book not found")
    updated = update_featured_book(db=db, db_obj=db_obj, obj_in=featured_in)
    return FeaturedBookResponse(
        id=updated.id,
        book_id=updated.book_id,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
        title=updated.book.title if updated.book else None,
        author=updated.book.author if updated.book else None,
        category_id=updated.book.category_id if updated.book else None,
        cover=updated.book.cover if updated.book else None,
    )

# ---------- DELETE ----------
@router.delete("/{featured_id}", response_model=dict)
def delete_featured(featured_id: int, db: Session = Depends(get_db)):
    db_obj = get_featured_book(db=db, featured_id=featured_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Featured book not found")
    delete_featured_book(db=db, db_obj=db_obj)
    return {"detail": "Featured book deleted successfully"}
