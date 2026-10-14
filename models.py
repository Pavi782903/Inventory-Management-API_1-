
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True
    )

    # Added in migration 003
    phone: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )
    address: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("1"),
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="supplier"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    price: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    stock_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Added in migration 002
    sku: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True
    )
    reorder_level: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10, server_default=text("10")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    category: Mapped["Category"] = relationship(
        back_populates="products"
    )
    supplier: Mapped["Supplier | None"] = relationship(
        back_populates="products"
    )
