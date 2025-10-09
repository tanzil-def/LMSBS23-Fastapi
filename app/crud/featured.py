from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.featured import FeaturedBook
from app.schemas.featured import FeaturedBookCreate, FeaturedBookUpdate

#   CREATE
def create_featured_book(db: Session, obj_in: FeaturedBookCreate) -> FeaturedBook:
    db_obj = FeaturedBook(book_id=obj_in.book_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # eager load book info
    db_obj.book  
    return db_obj

#   GET SINGLE
def get_featured_book(db: Session, featured_id: int) -> Optional[FeaturedBook]:
    return db.query(FeaturedBook).options(joinedload(FeaturedBook.book)).filter(FeaturedBook.id == featured_id).first()

#   GET ALL 
def get_featured_books(db: Session, skip: int = 0, limit: int = 100) -> List[FeaturedBook]:
    return db.query(FeaturedBook).options(joinedload(FeaturedBook.book)).offset(skip).limit(limit).all()

#   UPDATE 
def update_featured_book(db: Session, db_obj: FeaturedBook, obj_in: FeaturedBookUpdate) -> FeaturedBook:
    if obj_in.book_id is not None:
        db_obj.book_id = obj_in.book_id
    db.commit()
    db.refresh(db_obj)
    db_obj.book  
    return db_obj

#  DELETE 
def delete_featured_book(db: Session, db_obj: FeaturedBook) -> None:
    db.delete(db_obj)
    db.commit()
