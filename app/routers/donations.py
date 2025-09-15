from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import donation as donation_crud
from app.schemas import donation as donation_schema
from app.db.session import get_db

router = APIRouter(tags=["Donation Requests"])

@router.post("/create", response_model=donation_schema.DonationResponse, status_code=201)
def create_donation_request(request: donation_schema.DonationCreate, db: Session = Depends(get_db)):
    donation = donation_crud.create_donation_request(db, request)
    return donation

@router.get("/list", response_model=List[donation_schema.DonationResponse])
def get_all_donations(user_id: Optional[int] = None, status: Optional[donation_schema.DonationStatusEnum] = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return donation_crud.get_all_donation_requests(db, user_id, status, skip, limit)

@router.get("/retrieve/{id}", response_model=donation_schema.DonationResponse)
def retrieve_donation(id: int, db: Session = Depends(get_db)):
    donation = donation_crud.get_donation_request_by_id(db, id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation request not found")
    return donation

@router.put("/edit/{id}", response_model=donation_schema.DonationResponse)
def edit_donation(id: int, request: donation_schema.DonationUpdate, db: Session = Depends(get_db)):
    donation = donation_crud.update_donation_request(db, id, request)
    if not donation:
        raise HTTPException(status_code=400, detail="Cannot update donation request")
    return donation

@router.delete("/delete/{id}", status_code=204)
def delete_donation(id: int, db: Session = Depends(get_db)):
    success = donation_crud.delete_donation_request(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Cannot delete donation request")
    return None

@router.put("/status/{id}", response_model=donation_schema.DonationResponse)
def update_status(id: int, request: donation_schema.DonationStatusUpdate, db: Session = Depends(get_db)):
    donation = donation_crud.update_donation_status(db, id, request.status, request.admin_notes)
    if not donation:
        raise HTTPException(status_code=400, detail="Invalid status or donation not found")
    return donation

@router.get("/pending", response_model=List[donation_schema.DonationResponse])
def pending_donations(db: Session = Depends(get_db)):
    return donation_crud.get_requests_by_status(db, donation_schema.DonationStatusEnum.PENDING)

@router.get("/approved", response_model=List[donation_schema.DonationResponse])
def approved_donations(db: Session = Depends(get_db)):
    return donation_crud.get_requests_by_status(db, donation_schema.DonationStatusEnum.APPROVED)
