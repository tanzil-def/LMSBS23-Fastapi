from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import review as crud_review
from app.schemas.review import ReviewCreateRequest, ReviewUpdateRequest, ReviewResponse
from app.db.database import get_db

router = APIRouter(prefix="/api/review", tags=["Review Management"])

# Helper function: SQLAlchemy object থেকে Response dict বানাবে
def review_to_dict(review):
    return ReviewResponse(
        id=review.id,
        user={"id": review.user.id, "username": getattr(review.user, "username", "Unknown")},
        book={"id": review.book.id, "title": getattr(review.book, "title", "Unknown")},
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at.isoformat(),
        updated_at=review.updated_at.isoformat() if review.updated_at else None
    )

# Create review
@router.post("/book/{book_id}/create", response_model=ReviewResponse)
def create_review(book_id: int, review_in: ReviewCreateRequest, db: Session = Depends(get_db)):
    existing = crud_review.get_review_by_user_and_book(db, review_in.userId, book_id)
    if existing:
        raise HTTPException(status_code=409, detail="Review already exists")
    
    review = crud_review.create_review(db, book_id, review_in)
    db.refresh(review)
    return review_to_dict(review)

# Get single review
@router.get("/retrieve/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = crud_review.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review_to_dict(review)

# Get reviews by book
@router.get("/list/book/{book_id}", response_model=List[ReviewResponse])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = crud_review.get_reviews_by_book(db, book_id)
    return [review_to_dict(r) for r in reviews]

# Get reviews by user
@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    reviews = crud_review.get_reviews_by_user(db, user_id)
    return [review_to_dict(r) for r in reviews]

# Update review
@router.put("/edit/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review_in: ReviewUpdateRequest, db: Session = Depends(get_db)):
    review = crud_review.update_review(db, review_id, review_in)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.refresh(review)
    return review_to_dict(review)

# Delete review
@router.delete("/delete/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = crud_review.delete_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"detail": "Review deleted successfully"}

# Review stats for book
@router.get("/book/{book_id}/stats")
def get_review_stats(book_id: int, db: Session = Depends(get_db)):
    return crud_review.get_review_stats(db, book_id)
