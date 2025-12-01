# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routers import restaurants, menu_items, customers, orders, menu_categories, transcribe, tts
from fastapi.middleware.cors import CORSMiddleware

# Crear tablas en la DB (para entornos pequeños / dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CartaSmart API")

origins = [
    "http://localhost:3000",
    "http://localhost",
    "https://front-carta-smart-production.up.railway.app",   # tu FRONT en Railway
    "https://carta-smart-api-31496243302.europe-west1.run.app",  # tu BACK en Cloud Run
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(restaurants.router)
app.include_router(menu_items.router)
app.include_router(menu_categories.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(transcribe.router)
app.include_router(tts.router)




@app.get("/")
def read_root():
    return {"message": "CartaSmart API is running"}
