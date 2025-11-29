# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routers import restaurants, menu_items, customers, orders, menu_categories

# Crear tablas en la DB (para entornos pequeños / dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CartaSmart API")

app.include_router(restaurants.router)
app.include_router(menu_items.router)
app.include_router(menu_categories.router)
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/")
def read_root():
    return {"message": "CartaSmart API is running"}
