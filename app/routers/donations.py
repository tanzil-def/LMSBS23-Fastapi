from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import donation as donation_crud
from app.schemas import donation as donation_schema
from app.db.database import get_db

router = APIRouter(
    prefix="/api/donation-req",
    tags=["Donation Requests"]
)

@router.post("/create", response_model=donation_schema.DonationResponse, status_code=201)
def create_donation_request(request: donation_schema.DonationCreate, db: Session = Depends(get_db)):
    donation = donation_crud.create_donation_request(db, request)
    if not donation:
        raise HTTPException(status_code=400, detail="Invalid request or user not found")
    return donation

@router.get("/list", response_model=List[donation_schema.DonationResponse])
def get_all_donation_requests(
    user_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return donation_crud.get_all_donation_requests(db, user_id, status, skip, limit)

@router.get("/retrieve/{id}", response_model=donation_schema.DonationResponse)
def retrieve_donation_request(id: int, db: Session = Depends(get_db)):
    donation = donation_crud.get_donation_request_by_id(db, id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation request not found")
    return donation

@router.put("/edit/{id}", response_model=donation_schema.DonationResponse)
def update_donation_request(id: int, request: donation_schema.DonationUpdate, db: Session = Depends(get_db)):
    donation = donation_crud.update_donation_request(db, id, request)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation request not found or cannot be updated")
    return donation

@router.delete("/delete/{id}", status_code=204)
def delete_donation_request(id: int, db: Session = Depends(get_db)):
    success = donation_crud.delete_donation_request(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Donation request not found or cannot be deleted")
    return None

@router.post("/status/{id}", response_model=donation_schema.DonationResponse)
def update_donation_status(id: int, request: donation_schema.DonationStatusUpdate, db: Session = Depends(get_db)):
    donation = donation_crud.update_donation_status(db, id, request.status)
    if not donation:
        raise HTTPException(status_code=400, detail="Invalid status or donation not found")
    return donation

@router.get("/user/{user_id}", response_model=List[donation_schema.DonationResponse])
def get_user_donation_requests(user_id: int, status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return donation_crud.get_user_donation_requests(db, user_id, status)

@router.get("/pending", response_model=List[donation_schema.DonationResponse])
def get_pending_requests(db: Session = Depends(get_db)):
    return donation_crud.get_requests_by_status(db, "PENDING")

@router.get("/approved", response_model=List[donation_schema.DonationResponse])
def get_approved_requests(db: Session = Depends(get_db)):
    return donation_crud.get_requests_by_status(db, "APPROVED")

@router.put("/approve/{id}", response_model=donation_schema.DonationResponse)
def approve_request(id: int, admin_notes: Optional[str] = None, db: Session = Depends(get_db)):
    donation = donation_crud.approve_donation_request(db, id, admin_notes)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation request not found or cannot be approved")
    return donation

@router.put("/reject/{id}", response_model=donation_schema.DonationResponse)
def reject_request(id: int, admin_notes: Optional[str] = None, db: Session = Depends(get_db)):
    donation = donation_crud.reject_donation_request(db, id, admin_notes)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation request not found or cannot be rejected")
    return donation
