from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import List, Optional
from app.models.donation import DonationRequest, DonationStatus
from app.schemas import donation as donation_schema
from app.models.user import User  # Ensure correct import

def create_donation_request(db: Session, request: donation_schema.DonationCreate):
    donation = DonationRequest(
        user_id=request.user_id,
        book_title=request.book_title,
        author=request.author,
        isbn=request.isbn,
        notes=request.notes,
        status=DonationStatus.pending
    )
    db.add(donation)
    db.commit()
    db.refresh(donation)
    
    # Ensure user.full_name has value
    if donation.user and not donation.user.full_name:
        donation.user.full_name = donation.user.username

    donation.status = donation.status.value
    return donation

def get_all_donation_requests(
    db: Session,
    user_id: Optional[int] = None,
    status: Optional[donation_schema.DonationStatusEnum] = None,
    skip: int = 0,
    limit: int = 10
) -> List[DonationRequest]:
    query = db.query(DonationRequest).options(joinedload(DonationRequest.user))
    if user_id:
        query = query.filter(DonationRequest.user_id == user_id)
    if status:
        query = query.filter(DonationRequest.status == DonationStatus[status.value])
    
    donations = query.offset(skip).limit(limit).all()
    for donation in donations:
        if donation.user and not donation.user.full_name:
            donation.user.full_name = donation.user.username
        donation.status = donation.status.value
    return donations

def get_donation_request_by_id(db: Session, donation_id: int):
    donation = db.query(DonationRequest)\
                 .options(joinedload(DonationRequest.user))\
                 .filter(DonationRequest.id == donation_id).first()
    if donation:
        if donation.user and not donation.user.full_name:
            donation.user.full_name = donation.user.username
        donation.status = donation.status.value
    return donation

def update_donation_request(db: Session, donation_id: int, request: donation_schema.DonationUpdate):
    donation = get_donation_request_by_id(db, donation_id)
    if not donation or donation.status != DonationStatus.pending.value:
        return None
    
    donation.book_title = request.book_title
    donation.author = request.author
    donation.isbn = request.isbn
    donation.notes = request.notes
    donation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(donation)
    
    if donation.user and not donation.user.full_name:
        donation.user.full_name = donation.user.username
    donation.status = donation.status.value
    return donation

def delete_donation_request(db: Session, donation_id: int):
    donation = get_donation_request_by_id(db, donation_id)
    if not donation or donation.status != DonationStatus.pending.value:
        return False
    db.delete(donation)
    db.commit()
    return True

def update_donation_status(
    db: Session,
    donation_id: int,
    status: donation_schema.DonationStatusEnum,
    admin_notes: Optional[str] = None
):
    donation = get_donation_request_by_id(db, donation_id)
    if not donation:
        return None
    
    donation.status = DonationStatus[status.value]
    donation.admin_notes = admin_notes
    donation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(donation)
    
    if donation.user and not donation.user.full_name:
        donation.user.full_name = donation.user.username
    donation.status = donation.status.value
    return donation

def get_requests_by_status(db: Session, status: donation_schema.DonationStatusEnum) -> List[DonationRequest]:
    donations = db.query(DonationRequest)\
                  .options(joinedload(DonationRequest.user))\
                  .filter(DonationRequest.status == DonationStatus[status.value]).all()
    for donation in donations:
        if donation.user and not donation.user.full_name:
            donation.user.full_name = donation.user.username
        donation.status = donation.status.value
    return donations
