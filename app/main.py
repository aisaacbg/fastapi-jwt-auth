from fastapi import FastAPI
from . import models
from .database import SessionLocal, engine
from app.auth.routes import router as auth_router

# Initialize the FastAPI app
app = FastAPI()

# Create the database tables at the application startup
@app.on_event("startup")
def on_startup():
    print("Creating tables...")
    models.Base.metadata.create_all(bind=engine)  # Create tables on start app

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI JWT Auth!"}

# Register the auth routes without a prefix
app.include_router(auth_router)