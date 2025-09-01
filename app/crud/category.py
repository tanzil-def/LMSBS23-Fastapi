from sqlalchemy.orm import Session
from app.schemas import category as category_schema
from app.models.category import Category

def create_category(db: Session, request: category_schema.CategoryCreate):
    """Create new category"""
    existing = db.query(Category).filter(Category.name.ilike(request.name)).first()
    if existing:
        return None
    category = Category(name=request.name, description=request.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category_by_id(db: Session, category_id: int):
    """Get category by ID"""
    return db.query(Category).filter(Category.id == category_id).first()

def get_all_categories(db: Session, skip: int = 0, limit: int = 10):
    """Paginated categories"""
    return db.query(Category).offset(skip).limit(limit).all()

def get_all_categories_list(db: Session):
    """All categories as simple list"""
    return db.query(Category).all()

def update_category(db: Session, category_id: int, request: category_schema.CategoryUpdate):
    """Update existing category"""
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
    return category

def delete_category(db: Session, category_id: int):
    """Delete category if no books are associated"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return False

    if category.books and len(category.books) > 0:
        return False

    db.delete(category)
    db.commit()
    return True
