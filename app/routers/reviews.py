from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import review as crud_review
from app.schemas.review import ReviewCreateRequest, ReviewUpdateRequest, ReviewResponse
from app.db.database import get_db

router = APIRouter(prefix="/api/review", tags=["Review Management"])

@router.post("/book/{book_id}/create", response_model=ReviewResponse)
def create_review(book_id: int, review_in: ReviewCreateRequest, db: Session = Depends(get_db)):
    existing = crud_review.get_review_by_user_and_book(db, review_in.userId, book_id)
    if existing:
        raise HTTPException(status_code=409, detail="Review already exists")
    return crud_review.create_review(db, book_id, review_in)

@router.get("/list/book/{book_id}", response_model=List[ReviewResponse])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    return crud_review.get_reviews_by_book(db, book_id)

@router.get("/retrieve/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = crud_review.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/edit/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review_in: ReviewUpdateRequest, db: Session = Depends(get_db)):
    review = crud_review.update_review(db, review_id, review_in)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.delete("/delete/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = crud_review.delete_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"detail": "Review deleted successfully"}

@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    return crud_review.get_reviews_by_user(db, user_id)

@router.get("/book/{book_id}/stats")
def get_review_stats(book_id: int, db: Session = Depends(get_db)):
    return crud_review.get_review_stats(db, book_id)
