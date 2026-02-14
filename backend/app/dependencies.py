"""
Authentication dependencies and utilities
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional
from uuid import UUID
import logging

from app.config import get_settings
from app.database import get_db
from app.services.supabase import get_supabase_client
from app.models import User

settings = get_settings()
security = HTTPBearer()
logger = logging.getLogger(__name__)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Verify JWT token and return current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token with Supabase
        token = credentials.credentials
        supabase = get_supabase_client()
        
        # Get user from Supabase Auth
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise credentials_exception
        
        supabase_user = user_response.user
        
        # Get or create user in our database
        db_user = db.query(User).filter(User.id == UUID(supabase_user.id)).first()
        
        if not db_user:
            # Create user record if doesn't exist
            db_user = User(
                id=UUID(supabase_user.id),
                email=supabase_user.email,
                name=supabase_user.user_metadata.get("name", supabase_user.email),
                role=supabase_user.user_metadata.get("role", "student"),
                is_active=True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return db_user
        
    except Exception as e:
        logger.error(f"Auth error: {str(e)}")
        raise credentials_exception


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_role(allowed_roles: list):
    """Decorator to require specific roles"""
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


# Common role requirements
require_admin = require_role(["admin", "super-admin"])
require_faculty = require_role(["faculty", "admin", "super-admin"])
require_student = require_role(["student", "faculty", "admin", "super-admin"])
