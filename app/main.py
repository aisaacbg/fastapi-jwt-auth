from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import get_db, SessionLocal, engine
from datetime import timedelta
from jose import jwt
from .config import settings

# Initialize the FastAPI app
app = FastAPI()

# Create the database tables at the application startup
@app.on_event("startup")
def on_startup():
    print("Creating tables...")
    models.Base.metadata.create_all(bind=engine)  # Crear todas las tablas al iniciar la app

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

@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email_or_username(db, email=user.email, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token/refresh")
def refresh_token(current_user: schemas.UserOut = Depends(auth.get_current_user)):
    # Here we're using the current token to create a new one with a refreshed expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_token = auth.create_access_token(data={"sub": current_user.username}, expires_delta=access_token_expires)
    
    return {"access_token": new_token, "token_type": "bearer"}

@app.post("/token/verify")
def verify_token(authorization: str = Header(...)):
    token = authorization.split("Bearer ")[-1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"token": "valid"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
@app.post("/logout")
def logout(current_user: schemas.UserOut = Depends(auth.get_current_user), token: str = Depends(auth.oauth2_scheme)):
    return {"msg": "Logout successful"}
