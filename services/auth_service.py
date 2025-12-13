"""
Authentication service for user registration, login, and session management.

This service handles all authentication logic in standalone Streamlit architecture.
Uses SQLAlchemy for database access and session-based authentication.
"""
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from models.database import get_db, init_db
from models.user import User, UserProfile
from utils.security import hash_password, verify_password


class AuthService:
    """Authentication service for user management."""
    
    @staticmethod
    def register_user(email: str, password: str, name: str) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            email: User email address
            password: Plain text password (will be hashed)
            name: User's full name
            
        Returns:
            Dictionary with user data or error
            
        Raises:
            ValueError: If email already exists or validation fails
        """
        # Validate inputs
        if not email or not password or not name:
            raise ValueError("All fields are required")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Get database session
        db = next(get_db())
        
        try:
            # Check if email exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                raise ValueError("Email already registered")
            
            # Create new user
            new_user = User(
                email=email,
                password_hash=hash_password(password),
                name=name
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return {
                "success": True,
                "user_id": new_user.id,
                "email": new_user.email,
                "name": new_user.name
            }
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def login_user(email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and create session.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Dictionary with user data or error
            
        Raises:
            ValueError: If credentials are invalid
        """
        if not email or not password:
            raise ValueError("Email and password are required")
        
        db = next(get_db())
        
        try:
            # Find user
            user = db.query(User).filter(User.email == email).first()
            
            if not user or not verify_password(password, user.password_hash):
                raise ValueError("Invalid email or password")
            
            # Update last login
            user.last_login_at = datetime.utcnow()
            db.commit()
            
            return {
                "success": True,
                "user_id": user.id,
                "email": user.email,
                "name": user.name
            }
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def get_user(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User data dictionary or None
        """
        db = next(get_db())
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return None
            
            return {
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at
            }
            
        finally:
            db.close()
