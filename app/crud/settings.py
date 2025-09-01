# crud/settings.py
from sqlalchemy.orm import Session
from app.models.settings import AdminSettings
from typing import Optional

def get_settings(db: Session) -> AdminSettings:
    """Get the single admin settings row (create if not exists)"""
    settings = db.query(AdminSettings).first()
    if not settings:
        settings = AdminSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

def set_borrow_day_limit(db: Session, value: int) -> AdminSettings:
    settings = get_settings(db)
    settings.borrow_day_limit = value
    db.commit()
    db.refresh(settings)
    return settings

def set_borrow_extend_limit(db: Session, value: int) -> AdminSettings:
    settings = get_settings(db)
    settings.borrow_extend_limit = value
    db.commit()
    db.refresh(settings)
    return settings

def set_borrow_book_limit(db: Session, value: int) -> AdminSettings:
    settings = get_settings(db)
    settings.borrow_book_limit = value
    db.commit()
    db.refresh(settings)
    return settings

def set_booking_days_limit(db: Session, value: int) -> AdminSettings:
    settings = get_settings(db)
    settings.booking_days_limit = value
    db.commit()
    db.refresh(settings)
    return settings
