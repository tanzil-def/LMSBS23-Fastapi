from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.models.donation import DonationRequest, DonationStatus
from app.schemas import donation as donation_schema

def create_donation_request(db: Session, request: donation_schema.DonationCreate):
    donation = DonationRequest(
        user_id=request.user_id,
        book_title=request.book_title,
        author=request.author,
        notes=request.notes,
        status=DonationStatus.PENDING,
        created_at=datetime.utcnow()
    )
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

def get_all_donation_requests(db: Session, user_id: Optional[int], status: Optional[str], skip: int, limit: int):
    query = db.query(DonationRequest)
    if user_id:
        query = query.filter(DonationRequest.user_id == user_id)
    if status:
        query = query.filter(DonationRequest.status == status.upper())
    return query.offset(skip).limit(limit).all()

def get_donation_request_by_id(db: Session, donation_id: int):
    return db.query(DonationRequest).filter(DonationRequest.id == donation_id).first()

def update_donation_request(db: Session, donation_id: int, request: donation_schema.DonationUpdate):
    donation = get_donation_request_by_id(db, donation_id)
    if not donation or donation.status != DonationStatus.PENDING:
        return None
    donation.book_title = request.book_title
    donation.author = request.author
    donation.notes = request.notes
    db.commit()
    db.refresh(donation)
    return donation

def delete_donation_request(db: Session, donation_id: int):
    donation = get_donation_request_by_id(db, donation_id)
    if not donation or donation.status != DonationStatus.PENDING:
        return False
    db.delete(donation)
    db.commit()
    return True

def update_donation_status(db: Session, donation_id: int, status: str, admin_notes: Optional[str] = None):
    donation = get_donation_request_by_id(db, donation_id)
    if not donation:
        return None
    donation.status = DonationStatus[status.upper()]
    donation.admin_notes = admin_notes
    donation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(donation)
    return donation

def get_user_donation_requests(db: Session, user_id: int, status: Optional[str]):
    query = db.query(DonationRequest).filter(DonationRequest.user_id == user_id)
    if status:
        query = query.filter(DonationRequest.status == status.upper())
    return query.all()

def get_requests_by_status(db: Session, status: str):
    return db.query(DonationRequest).filter(DonationRequest.status == status.upper()).all()

def approve_donation_request(db: Session, donation_id: int, admin_notes: Optional[str]):
    return update_donation_status(db, donation_id, "APPROVED", admin_notes)

def reject_donation_request(db: Session, donation_id: int, admin_notes: Optional[str]):
    return update_donation_status(db, donation_id, "REJECTED", admin_notes)
