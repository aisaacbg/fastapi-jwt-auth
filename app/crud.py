from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email_or_username(db: Session, email: str, username: str):
    return db.query(models.User).filter(
        (models.User.email == email) | (models.User.username == username)
    ).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email_or_username(db, email=email, username=email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user
