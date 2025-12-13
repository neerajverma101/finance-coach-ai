"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from backend.models.user import RiskProfile, FinancialKnowledge


# ============ Auth Schemas ============

class UserRegister(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=2, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    expires_in: int


class TokenData(BaseModel):
    """Decoded token data."""
    user_id: Optional[str] = None


# ============ Profile Schemas ============

class ProfileCreate(BaseModel):
    """Create/update user profile."""
    age: Optional[int] = Field(None, ge=18, le=100)
    country: str = Field(default="India")
    dependents: int = Field(default=0, ge=0, le=20)
    risk_profile: Optional[RiskProfile] = None
    financial_knowledge: Optional[FinancialKnowledge] = None


class ProfileResponse(BaseModel):
    """User profile response."""
    user_id: str
    age: Optional[int]
    country: str
    dependents: int
    risk_profile: Optional[RiskProfile]
    financial_knowledge: Optional[FinancialKnowledge]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User information response."""
    id: str
    email: str
    name: str
    created_at: datetime
    profile_complete: bool
    
    class Config:
        from_attributes = True


# ============ Response Wrapper ============

class SuccessResponse(BaseModel):
    """Standard success response wrapper."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: dict
