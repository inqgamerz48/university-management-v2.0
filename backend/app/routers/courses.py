"""
Courses Router
Handles course management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.dependencies import get_current_user, require_admin, require_faculty
from app.schemas import (
    CourseCreate, CourseUpdate, CourseResponse, CourseWithDetails,
    EnrollmentCreate, EnrollmentResponse, MessageResponse
)
from app.models import Course, CourseEnrollment, User, Department

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=List[CourseWithDetails])
async def list_courses(
    department_id: Optional[int] = Query(None),
    faculty_id: Optional[UUID] = Query(None),
    semester: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all courses
    """
    query = db.query(Course).filter(Course.is_active == True)
    
    # Apply filters
    if department_id:
        query = query.filter(Course.department_id == department_id)
    if faculty_id:
        query = query.filter(Course.faculty_id == faculty_id)
    if semester:
        query = query.filter(Course.semester == semester)
    if year:
        query = query.filter(Course.year == year)
    if search:
        query = query.filter(
            (Course.name.ilike(f"%{search}%")) | 
            (Course.code.ilike(f"%{search}%"))
        )
    
    courses = query.offset(skip).limit(limit).all()
    
    # Enrich with details
    result = []
    for course in courses:
        course_data = CourseWithDetails.from_orm(course)
        course_data.enrolled_count = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course.id
        ).count()
        result.append(course_data)
    
    return result


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Create a new course (faculty and admin only)
    """
    # Check if course code already exists
    existing = db.query(Course).filter(Course.code == course_data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this code already exists"
        )
    
    new_course = Course(**course_data.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course


@router.get("/{course_id}", response_model=CourseWithDetails)
async def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get course by ID
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    course_data = CourseWithDetails.from_orm(course)
    course_data.enrolled_count = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course.id
    ).count()
    
    return course_data


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Update course (faculty who teaches it or admin)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions - faculty can only update their own courses
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update courses you teach"
        )
    
    # Update fields
    for field, value in course_update.dict(exclude_unset=True).items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete course (admin only)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Soft delete
    course.is_active = False
    db.commit()
    
    return None


# ============== Enrollment Endpoints ==============

@router.get("/{course_id}/enrollments", response_model=List[dict])
async def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Get all students enrolled in a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id
    ).all()
    
    result = []
    for enrollment in enrollments:
        student = db.query(User).filter(User.id == enrollment.student_id).first()
        if student:
            result.append({
                "enrollment_id": enrollment.id,
                "student_id": student.id,
                "student_name": student.name,
                "student_email": student.email,
                "status": enrollment.status,
                "enrolled_at": enrollment.enrolled_at
            })
    
    return result


@router.post("/{course_id}/enroll", response_model=EnrollmentResponse)
async def enroll_student(
    course_id: int,
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Enroll a student in a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if already enrolled
    existing = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.student_id == student_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already enrolled in this course"
        )
    
    enrollment = CourseEnrollment(
        course_id=course_id,
        student_id=student_id
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return enrollment


@router.post("/{course_id}/enrollments/bulk", response_model=MessageResponse)
async def bulk_enroll(
    course_id: int,
    student_ids: List[UUID],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Bulk enroll students (admin only)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    enrolled_count = 0
    for student_id in student_ids:
        existing = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id,
            CourseEnrollment.student_id == student_id
        ).first()
        
        if not existing:
            enrollment = CourseEnrollment(
                course_id=course_id,
                student_id=student_id
            )
            db.add(enrollment)
            enrolled_count += 1
    
    db.commit()
    
    return {
        "message": f"Successfully enrolled {enrolled_count} students",
        "success": True
    }


@router.delete("/{course_id}/enrollments/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll_student(
    course_id: int,
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Remove a student from a course
    """
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.student_id == student_id
    ).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    db.delete(enrollment)
    db.commit()
    
    return None
