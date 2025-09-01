from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

# ---------------------------
# Notification type enum
# ---------------------------
class NotificationTypeEnum(str, Enum):
    INFO = "INFO"
    ALERT = "ALERT"
    WARNING = "WARNING"

# ---------------------------
# Request Schemas
# ---------------------------
class NotificationCreate(BaseModel):
    recipient_id: int = Field(..., description="ID of the user who will receive the notification")
    title: str = Field(..., max_length=255, description="Title of the notification")
    message: str = Field(..., max_length=1000, description="Content of the notification")
    type: Optional[NotificationTypeEnum] = Field(NotificationTypeEnum.INFO, description="Type of notification, default INFO")
    is_read: Optional[bool] = Field(False, description="Whether the notification is already read")

class NotificationUpdate(BaseModel):
    is_read: bool = Field(..., description="Mark notification as read/unread")

class EmailNotificationRequest(BaseModel):
    to: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., max_length=255, description="Email subject")
    text: str = Field(..., max_length=2000, description="Email body content")

# ---------------------------
# Response Schema
# ---------------------------
class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    title: str
    message: str
    type: NotificationTypeEnum
    is_read: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
