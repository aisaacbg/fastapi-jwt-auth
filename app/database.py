from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import os

# Verifica si los tests están corriendo
is_testing = os.getenv("PYTEST_CURRENT_TEST") is not None

# Usa la base de datos de pruebas si está corriendo pytest
if is_testing:
    SQLALCHEMY_DATABASE_URL = settings.TEST_SQLALCHEMY_DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
