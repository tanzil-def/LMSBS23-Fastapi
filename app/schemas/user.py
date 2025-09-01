# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class RegisterRequest(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.USER

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str
    type: str = "Bearer"
    id: int
    email: EmailStr
    username: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
