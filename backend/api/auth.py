"""
Authentication API endpoints: register, login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.database import get_db
from backend.models.user import User
from backend.api.schemas import UserRegister, UserLogin, Token, SuccessResponse
from backend.api.dependencies import get_current_user
from backend.utils.security import hash_password, verify_password, create_access_token
from backend.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user_data: User registration data (email, password, name)
        db: Database session
        
    Returns:
        JWT access token and user information
        
    Raises:
        HTTPException 409: Email already exists
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "EMAIL_EXISTS",
                "message": "An account with this email already exists"
            }
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.id})
    
    return Token(
        access_token=access_token,
        user_id=new_user.id,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    
    Args:
        credentials: User login credentials (email, password)
        db: Database session
        
    Returns:
        JWT access token and user information
        
    Raises:
        HTTPException 401: Invalid credentials
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        )
    
    # Update last login time
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    # Check if profile is complete
    profile_complete = user.profile is not None
    
    return Token(
        access_token=access_token,
        user_id=user.id,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/verify", response_model=SuccessResponse)
def verify_token(user: User = Depends(get_current_user)):
    """
    Verify if the current token is valid.
    
    Args:
        user: Current authenticated user (from token)
        
    Returns:
        Success response with user ID
    """
    return SuccessResponse(
        message="Token is valid",
        data={"user_id": user.id, "email": user.email}
    )
