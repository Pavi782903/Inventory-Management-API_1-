
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**data.model_dump())
    db.add(category)

    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Category name already exists")


@router.get("", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id).all()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)

    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Category name already exists")


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    db.delete(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409, "Cannot delete a category that has products"
        )
