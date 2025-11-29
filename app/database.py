# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Para desarrollo local (SQLite). Se puede sobreescribir con DATABASE_URL
DEFAULT_SQLITE_URL = "sqlite:///./cartasmart.db"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# echo=True solo si quieres ver el SQL en consola
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,     # 👈 prueba conexión antes de usarla
    pool_recycle=1800 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
