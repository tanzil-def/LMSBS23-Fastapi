from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from app.models.review import Review
from app.schemas.review import ReviewCreateRequest, ReviewUpdateRequest
from app.models.user import User
from app.models.book import Book

def get_reviews_by_user(db: Session, user_id: int) -> List[Review]:
    return db.query(Review).filter(Review.user_id == user_id).all()

def get_reviews_by_book(db: Session, book_id: int) -> List[Review]:
    return db.query(Review).filter(Review.book_id == book_id).all()

def get_review_by_user_and_book(db: Session, user_id: int, book_id: int) -> Optional[Review]:
    return db.query(Review).filter(Review.user_id == user_id, Review.book_id == book_id).first()

def get_review(db: Session, review_id: int) -> Optional[Review]:
    return db.query(Review).filter(Review.id == review_id).first()

def create_review(db: Session, book_id: int, review_in: ReviewCreateRequest) -> Review:
    review = Review(
        user_id=review_in.userId,
        book_id=book_id,
        rating=review_in.rating,
        comment=review_in.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def update_review(db: Session, review_id: int, review_in: ReviewUpdateRequest) -> Optional[Review]:
    review = get_review(db, review_id)
    if review:
        if review_in.rating is not None:
            review.rating = review_in.rating
        if review_in.comment is not None:
            review.comment = review_in.comment
        db.commit()
        db.refresh(review)
    return review

def delete_review(db: Session, review_id: int):
    review = get_review(db, review_id)
    if review:
        db.delete(review)
        db.commit()
    return review

def get_review_stats(db: Session, book_id: int):
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.book_id == book_id).scalar() or 0
    total_reviews = db.query(Review).filter(Review.book_id == book_id).count()
    return {"average_rating": avg_rating, "total_reviews": total_reviews}
