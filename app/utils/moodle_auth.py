from sqlalchemy.orm import Session
from app import crud

def moodle_authenticate(db: Session, username: str, password: str):
    # Replace with actual Moodle LMS verification logic
    # For now, just fetch user by username
    return crud.user.get_user_by_username(db, username)
