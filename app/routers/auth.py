from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import RegisterRequest, LoginRequest, AuthResponse, UserRole
from app.crud import user as crud_user
from app.db.database import get_db
from app.core.jwt import create_access_token

# ✅ Only resource prefix here
router = APIRouter(prefix="/auth", tags=["Authentication"])

# --------------------------
# Register a new user
# --------------------------
@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = crud_user.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = crud_user.create_user(db, request, role=UserRole.USER)
    token = create_access_token({"sub": user.username, "role": user.role})
    return AuthResponse(
        token=token,
        id=user.id,
        email=user.email,
        username=user.username,
        role=user.role
    )

# --------------------------
# Register a new admin user
# --------------------------
@router.post("/register-admin", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_admin(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = crud_user.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = crud_user.create_user(db, request, role=UserRole.ADMIN)
    token = create_access_token({"sub": user.username, "role": user.role})
    return AuthResponse(
        token=token,
        id=user.id,
        email=user.email,
        username=user.username,
        role=user.role
    )

# --------------------------
# Login user
# --------------------------
@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role})
    return AuthResponse(
        token=token,
        id=user.id,
        email=user.email,
        username=user.username,
        role=user.role
    )
