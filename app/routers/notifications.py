from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.crud import notification as crud_notification
from app.schemas.notification import NotificationCreate, NotificationResponse, EmailNotificationRequest

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)

# ✅ Create Notification
@router.post("/create", response_model=NotificationResponse)
def create_notification(request: NotificationCreate, db: Session = Depends(get_db)):
    return crud_notification.create_notification(db=db, notification_in=request)

# ✅ Get Unread Notifications
@router.get("/unread/{recipient}", response_model=List[NotificationResponse])
def get_unread_notifications(recipient: str, db: Session = Depends(get_db)):
    return crud_notification.get_unread_notifications(db=db, recipient=recipient)

# ✅ Mark Notification as Read
@router.post("/mark-as-read/{id}", response_model=NotificationResponse)
def mark_notification_as_read(id: int, db: Session = Depends(get_db)):
    notification = crud_notification.mark_as_read(db=db, notification_id=id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

# ✅ Send Email Notification (placeholder service)
@router.post("/send-email")
def send_email_notification(request: EmailNotificationRequest):

    return {"message": f"Notification sent to {request.to}"}
