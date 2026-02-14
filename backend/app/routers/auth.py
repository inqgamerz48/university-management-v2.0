"""
Authentication Router
Handles login, signup, password reset
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.services.supabase import get_supabase_client, get_supabase_admin_client
from app.schemas import (
    UserCreate, UserResponse, UserLogin, TokenResponse,
    PasswordResetRequest, PasswordResetConfirm, MessageResponse
)
from app.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    try:
        supabase_admin = get_supabase_admin_client()
        
        # Create user in Supabase Auth
        auth_response = supabase_admin.auth.admin.create_user({
            "email": user_data.email,
            "password": user_data.password,
            "email_confirm": True,
            "user_metadata": {
                "name": user_data.name,
                "role": user_data.role
            }
        })
        
        if not auth_response or not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
        
        # Create user in our database
        from uuid import UUID
        new_user = User(
            id=UUID(auth_response.user.id),
            email=user_data.email,
            name=user_data.name,
            role=user_data.role,
            department=user_data.department,
            phone=user_data.phone,
            bio=user_data.bio,
            avatar_url=user_data.avatar_url,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Login user and return access token
    """
    try:
        supabase = get_supabase_client()
        
        auth_response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        if not auth_response or not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Build user response
        user_data = {
            "id": auth_response.user.id,
            "email": auth_response.user.email,
            "name": auth_response.user.user_metadata.get("name", auth_response.user.email),
            "role": auth_response.user.user_metadata.get("role", "student"),
            "is_active": True,
            "created_at": auth_response.user.created_at,
            "updated_at": auth_response.user.updated_at
        }
        
        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "token_type": "bearer",
            "expires_in": auth_response.session.expires_in,
            "user": user_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
        
        return {"message": "Successfully logged out", "success": True}
        
    except Exception as e:
        return {"message": f"Logout error: {str(e)}", "success": False}


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """
    Refresh access token
    """
    try:
        supabase = get_supabase_client()
        auth_response = supabase.auth.refresh_session(refresh_token)
        
        if not auth_response or not auth_response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "token_type": "bearer",
            "expires_in": auth_response.session.expires_in
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/password-reset-request", response_model=MessageResponse)
async def request_password_reset(request: PasswordResetRequest):
    """
    Request password reset email
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.reset_password_email(request.email)
        
        return {
            "message": "Password reset email sent. Check your inbox.",
            "success": True
        }
        
    except Exception as e:
        # Don't reveal if email exists
        return {
            "message": "If the email exists, a reset link has been sent.",
            "success": True
        }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user info
    """
    return current_user
