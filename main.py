
from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers import categories, products, suppliers

app = FastAPI(
    title="Inventory Management API",
    description="Inventory API with SQLAlchemy, MySQL, and Alembic",
    version="2.0.0",
)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(suppliers.router)


@app.get("/", tags=["Health"])
def home():
    return {"message": "Inventory Management API is running"}


@app.get("/health/db", tags=["Health"])
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"database": "connected"}
