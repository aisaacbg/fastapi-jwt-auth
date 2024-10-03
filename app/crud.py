from sqlalchemy.orm import Session, or_
from .models import User
from .schemas import UserCreate
from .auth import get_password_hash, verify_password

# GET user by email or username
def get_user_by_email_or_username(db: Session, email: str = None, username: str = None):
    return db.query(User).filter(or_(User.email == email, User.username == username)).first()

# Create new user
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Autenticate usuer
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
