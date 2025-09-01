from sqlalchemy.orm import Session
from typing import List
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

def create_notification(db: Session, notification_in: NotificationCreate) -> Notification:
    notification = Notification(
        recipient_id=notification_in.recipient_id,
        title=notification_in.title,
        message=notification_in.message,
        type=notification_in.type,
        is_read=notification_in.is_read
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_unread_notifications(db: Session, recipient: str) -> List[Notification]:
    return db.query(Notification).filter(Notification.recipient == recipient, Notification.is_read == False).all()

def mark_as_read(db: Session, notification_id: int) -> Notification | None:
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification
