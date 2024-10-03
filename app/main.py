from fastapi import FastAPI
from .database import engine
from . import models

# Create table if not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI JWT Auth!"}
