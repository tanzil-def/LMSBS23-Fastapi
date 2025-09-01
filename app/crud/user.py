# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import RegisterRequest
from app.models.user_role import UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_in: RegisterRequest):
    hashed_password = pwd_context.hash(user_in.password)
    db_user = User(
        username=user_in.username,
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
        role=user_in.role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user
