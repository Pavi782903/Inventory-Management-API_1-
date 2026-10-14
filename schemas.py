
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Categories ----------

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


# ---------- Products ----------

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: int
    supplier_id: int | None = None

    sku: str = Field(min_length=1, max_length=64)
    reorder_level: int = Field(default=10, ge=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(
        default=None, gt=0, max_digits=12, decimal_places=2
    )
    stock_quantity: int | None = Field(default=None, ge=0)
    category_id: int | None = None
    supplier_id: int | None = None

    sku: str | None = Field(default=None, min_length=1, max_length=64)
    reorder_level: int | None = Field(default=None, ge=0)


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    category_id: int
    supplier_id: int | None
    sku: str
    reorder_level: int
    updated_at: datetime


# ---------- Suppliers ----------

class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = None
    is_active: bool = True


class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = None
    is_active: bool | None = None


class SupplierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr | None
    phone: str | None
    address: str | None
    is_active: bool
