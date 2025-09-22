# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import user as crud_user
from app.models.user import User, UserRoleEnum
from app.schemas.user import RegisterRequest, LoginRequest, AuthResponse
from app.utils.security import create_access_token, decode_access_token

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ==========================
# JWT / Auth helpers
# ==========================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    username = payload.get("sub")
    role = payload.get("role")

    user = crud_user.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    user.role_value = role  # attach role to user object
    return user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role_value != UserRoleEnum.ADMIN.value:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# ==========================
# Endpoints
# ==========================
@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = crud_user.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = crud_user.create_user(db, request, role=UserRoleEnum.USER)
    token = create_access_token({"sub": user.username, "role": user.role.value})
    return AuthResponse(token=token, id=user.id, email=user.email, username=user.username, role=user.role.value)

@router.post("/register-admin", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_admin(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = crud_user.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = crud_user.create_user(db, request, role=UserRoleEnum.ADMIN)
    token = create_access_token({"sub": user.username, "role": user.role.value})
    return AuthResponse(token=token, id=user.id, email=user.email, username=user.username, role=user.role.value)

@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role.value})
    return AuthResponse(token=token, id=user.id, email=user.email, username=user.username, role=user.role.value)
