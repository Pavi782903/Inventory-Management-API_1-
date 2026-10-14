
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Supplier
from app.schemas import SupplierCreate, SupplierOut, SupplierUpdate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post("", response_model=SupplierOut, status_code=201)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**data.model_dump())
    db.add(supplier)

    try:
        db.commit()
        db.refresh(supplier)
        return supplier
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Supplier conflicts with a database constraint")


@router.get("", response_model=list[SupplierOut])
def get_suppliers(
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    statement = select(Supplier)

    if active_only:
        statement = statement.where(Supplier.is_active.is_(True))

    return db.scalars(statement.order_by(Supplier.id)).all()


@router.get("/{supplier_id}", response_model=SupplierOut)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(404, "Supplier not found")
    return supplier


@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    db: Session = Depends(get_db),
):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(404, "Supplier not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(supplier, field, value)

    try:
        db.commit()
        db.refresh(supplier)
        return supplier
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Supplier conflicts with a database constraint")


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(404, "Supplier not found")

    db.delete(supplier)
    db.commit()
