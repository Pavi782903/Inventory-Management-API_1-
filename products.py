
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Category, Product, Supplier
from app.schemas import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    if not db.get(Category, data.category_id):
        raise HTTPException(400, "The specified category does not exist")

    if data.supplier_id is not None and not db.get(Supplier, data.supplier_id):
        raise HTTPException(400, "The specified supplier does not exist")

    product = Product(**data.model_dump())
    db.add(product)

    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError as exc:
        db.rollback()
        message = str(exc.orig).lower()
        if "sku" in message:
            raise HTTPException(409, "A product with this SKU already exists")
        raise HTTPException(409, "Product conflicts with a database constraint")


@router.get("", response_model=list[ProductOut])
def get_products(
    category_id: int | None = None,
    supplier_id: int | None = None,
    needs_restock: bool = False,
    db: Session = Depends(get_db),
):
    statement = select(Product)

    if category_id is not None:
        statement = statement.where(Product.category_id == category_id)

    if supplier_id is not None:
        statement = statement.where(Product.supplier_id == supplier_id)

    if needs_restock:
        statement = statement.where(
            Product.stock_quantity <= Product.reorder_level
        )

    return db.scalars(statement.order_by(Product.id)).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    changes = data.model_dump(exclude_unset=True)

    if "category_id" in changes and changes["category_id"] is not None:
        if not db.get(Category, changes["category_id"]):
            raise HTTPException(400, "The specified category does not exist")

    if "supplier_id" in changes and changes["supplier_id"] is not None:
        if not db.get(Supplier, changes["supplier_id"]):
            raise HTTPException(400, "The specified supplier does not exist")

    for field, value in changes.items():
        setattr(product, field, value)

    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError as exc:
        db.rollback()
        message = str(exc.orig).lower()
        if "sku" in message:
            raise HTTPException(409, "A product with this SKU already exists")
        raise HTTPException(409, "Product conflicts with a database constraint")


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    db.delete(product)
    db.commit()
