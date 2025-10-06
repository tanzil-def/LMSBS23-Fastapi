from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import category as category_crud
from app.schemas import category as category_schema
from app.db.database import get_db

router = APIRouter(tags=["Category Management"])

# ✅ Create Category
@router.post("/create", response_model=category_schema.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(request: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    category = category_crud.create_category(db, request)
    if not category:
        raise HTTPException(status_code=409, detail="Category already exists")
    return category

# ✅ List all categories (static path BEFORE dynamic /{id})
@router.get("/list", response_model=List[category_schema.CategoryResponse])
def get_all_categories_list(db: Session = Depends(get_db)):
    return category_crud.get_all_categories_list(db)

# ✅ Get all categories with pagination
@router.get("", response_model=List[category_schema.CategoryResponse])
def get_all_categories(skip: int = 0, limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    return category_crud.get_all_categories(db, skip=skip, limit=limit)

# ✅ Get category by ID (dynamic path)
@router.get("/{id}", response_model=category_schema.CategoryResponse)
def get_category_by_id(id: int = Path(...), db: Session = Depends(get_db)):
    category = category_crud.get_category_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# ✅ Update category
@router.put("/edit/{id}", response_model=category_schema.CategoryResponse)
def update_category(id: int, request: category_schema.CategoryUpdate, db: Session = Depends(get_db)):
    category = category_crud.update_category(db, id, request)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found or name already exists")
    return category

# ✅ Delete category with success message
@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
def delete_category(id: int, db: Session = Depends(get_db)):
    success = category_crud.delete_category(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found or has associated books")
    return {"detail": "Category deleted successfully"}
