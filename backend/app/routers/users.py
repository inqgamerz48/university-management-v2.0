"""
Users Router
Handles user management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.dependencies import get_current_user, require_admin, require_faculty
from app.schemas import UserResponse, UserUpdate, PaginatedResponse
from app.models import User, CourseEnrollment, Course

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def list_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    department: Optional[str] = Query(None, description="Filter by department"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    List all users (faculty and admin only)
    """
    query = db.query(User)
    
    # Apply filters
    if role:
        query = query.filter(User.role == role)
    if department:
        query = query.filter(User.department.ilike(f"%{department}%"))
    if search:
        query = query.filter(
            (User.name.ilike(f"%{search}%")) | 
            (User.email.ilike(f"%{search}%"))
        )
    
    # Students can only see faculty in their courses
    if current_user.role == "student":
        # Get student's enrolled courses
        enrolled_course_ids = [
            enrollment.course_id 
            for enrollment in db.query(CourseEnrollment).filter(
                CourseEnrollment.student_id == current_user.id
            ).all()
        ]
        
        # Get faculty teaching those courses
        faculty_ids = [
            course.faculty_id 
            for course in db.query(Course).filter(
                Course.id.in_(enrolled_course_ids)
            ).all()
        ]
        
        query = query.filter(User.id.in_(faculty_ids))
    
    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID
    """
    # Users can view their own profile
    # Faculty can view students in their courses
    # Admins can view anyone
    
    if str(current_user.id) != str(user_id) and current_user.role not in ["faculty", "admin", "super-admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user profile
    """
    # Users can only update their own profile (unless admin)
    if str(current_user.id) != str(user_id) and current_user.role not in ["admin", "super-admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete user (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent self-deletion
    if str(user.id) == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Soft delete by deactivating
    user.is_active = False
    db.commit()
    
    return None


@router.get("/{user_id}/courses", response_model=List[dict])
async def get_user_courses(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get courses for a user (student enrollments or faculty teachings)
    """
    # Check permissions
    if str(current_user.id) != str(user_id) and current_user.role not in ["faculty", "admin", "super-admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role == "student":
        # Get enrolled courses
        enrollments = db.query(CourseEnrollment).filter(
            CourseEnrollment.student_id == user_id
        ).all()
        
        courses = []
        for enrollment in enrollments:
            course = db.query(Course).filter(Course.id == enrollment.course_id).first()
            if course:
                courses.append({
                    "id": course.id,
                    "name": course.name,
                    "code": course.code,
                    "credits": course.credits,
                    "status": enrollment.status,
                    "enrolled_at": enrollment.enrolled_at
                })
        
        return courses
    else:
        # Get taught courses
        courses = db.query(Course).filter(Course.faculty_id == user_id).all()
        
        return [
            {
                "id": course.id,
                "name": course.name,
                "code": course.code,
                "credits": course.credits,
                "semester": course.semester,
                "year": course.year
            }
            for course in courses
        ]
