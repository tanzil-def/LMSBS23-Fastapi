from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas import category as category_schema

def create_category(db: Session, request: category_schema.CategoryCreate):
    existing = db.query(Category).filter(Category.name.ilike(request.name)).first()
    if existing:
        return None

    category = Category(name=request.name, description=request.description)
    db.add(category)
    db.commit()
    db.refresh(category)

    # Set book_count dynamically for response
    category.book_count = len(category.books)  # usually 0 for new category
    return category

def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.book_count = len(category.books)
    return category

def get_all_categories(db: Session, skip: int = 0, limit: int = 10):
    categories = db.query(Category).offset(skip).limit(limit).all()
    for c in categories:
        c.book_count = len(c.books)
    return categories

def get_all_categories_list(db: Session):
    categories = db.query(Category).all()
    for c in categories:
        c.book_count = len(c.books)
    return categories

def update_category(db: Session, category_id: int, request: category_schema.CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return None

    duplicate = db.query(Category).filter(Category.name.ilike(request.name), Category.id != category_id).first()
    if duplicate:
        return None

    category.name = request.name
    category.description = request.description
    db.commit()
    db.refresh(category)

    category.book_count = len(category.books)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return False

    if category.books and len(category.books) > 0:
        return False

    db.delete(category)
    db.commit()
    return True
