"""
Assignments Router
Handles assignment management and submissions
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_user, require_faculty
from app.schemas import (
    AssignmentCreate, AssignmentUpdate, AssignmentResponse, AssignmentWithCourse,
    SubmissionCreate, SubmissionUpdate, SubmissionResponse, SubmissionWithDetails,
    MessageResponse
)
from app.models import Assignment, Submission, Course, CourseEnrollment, User
from app.services.storage import upload_file_to_storage

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get("/", response_model=List[AssignmentWithCourse])
async def list_assignments(
    course_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None, description="Filter by status: upcoming, overdue, all"),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List assignments
    """
    query = db.query(Assignment).filter(Assignment.is_published == True)
    
    # Apply filters
    if course_id:
        query = query.filter(Assignment.course_id == course_id)
    
    if status == "upcoming":
        query = query.filter(Assignment.due_date > datetime.now())
    elif status == "overdue":
        query = query.filter(Assignment.due_date < datetime.now())
    
    if search:
        query = query.filter(Assignment.title.ilike(f"%{search}%"))
    
    # Students only see assignments for enrolled courses
    if current_user.role == "student":
        enrolled_course_ids = [
            enrollment.course_id 
            for enrollment in db.query(CourseEnrollment).filter(
                CourseEnrollment.student_id == current_user.id
            ).all()
        ]
        query = query.filter(Assignment.course_id.in_(enrolled_course_ids))
    
    # Faculty only see their course assignments
    elif current_user.role == "faculty":
        faculty_course_ids = [
            course.id 
            for course in db.query(Course).filter(
                Course.faculty_id == current_user.id
            ).all()
        ]
        query = query.filter(Assignment.course_id.in_(faculty_course_ids))
    
    assignments = query.order_by(Assignment.due_date).offset(skip).limit(limit).all()
    
    return assignments


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Create a new assignment
    """
    # Verify course exists and user has permission
    course = db.query(Course).filter(Course.id == assignment_data.course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create assignments for courses you teach"
        )
    
    new_assignment = Assignment(
        **assignment_data.dict(),
        created_by=current_user.id
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return new_assignment


@router.get("/{assignment_id}", response_model=AssignmentWithCourse)
async def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get assignment by ID
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check access permissions
    if current_user.role == "student":
        enrollment = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == assignment.course_id,
            CourseEnrollment.student_id == current_user.id
        ).first()
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    return assignment


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Update assignment
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check permissions
    course = db.query(Course).filter(Course.id == assignment.course_id).first()
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update assignments for courses you teach"
        )
    
    for field, value in assignment_update.dict(exclude_unset=True).items():
        setattr(assignment, field, value)
    
    db.commit()
    db.refresh(assignment)
    
    return assignment


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Delete assignment
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check permissions
    course = db.query(Course).filter(Course.id == assignment.course_id).first()
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete assignments for courses you teach"
        )
    
    db.delete(assignment)
    db.commit()
    
    return None


# ============== Submission Endpoints ==============

@router.get("/{assignment_id}/submissions", response_model=List[SubmissionWithDetails])
async def get_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Get all submissions for an assignment (faculty only)
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check permissions
    course = db.query(Course).filter(Course.id == assignment.course_id).first()
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    submissions = db.query(Submission).filter(
        Submission.assignment_id == assignment_id
    ).all()
    
    return submissions


@router.get("/{assignment_id}/my-submission", response_model=Optional[SubmissionResponse])
async def get_my_submission(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's submission for an assignment
    """
    submission = db.query(Submission).filter(
        Submission.assignment_id == assignment_id,
        Submission.student_id == current_user.id
    ).first()
    
    return submission


@router.post("/{assignment_id}/submit", response_model=SubmissionResponse)
async def submit_assignment(
    assignment_id: int,
    comments: Optional[str] = None,
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit an assignment
    """
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can submit assignments"
        )
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check if student is enrolled
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == assignment.course_id,
        CourseEnrollment.student_id == current_user.id
    ).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not enrolled in this course"
        )
    
    # Check if already submitted
    existing = db.query(Submission).filter(
        Submission.assignment_id == assignment_id,
        Submission.student_id == current_user.id
    ).first()
    
    file_url = None
    file_name = None
    file_size = None
    
    if file:
        # Upload file to storage
        upload_result = await upload_file_to_storage(
            file,
            folder=f"assignments/{assignment_id}",
            user_id=current_user.id
        )
        file_url = upload_result["url"]
        file_name = upload_result["file_name"]
        file_size = upload_result["file_size"]
    
    # Determine if late
    status = "submitted"
    if assignment.due_date and datetime.now() > assignment.due_date:
        status = "late"
    
    if existing:
        # Update existing submission
        existing.comments = comments
        if file_url:
            existing.file_url = file_url
            existing.file_name = file_name
            existing.file_size = file_size
        existing.submitted_at = datetime.now()
        existing.status = status
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new submission
        submission = Submission(
            assignment_id=assignment_id,
            student_id=current_user.id,
            file_url=file_url,
            file_name=file_name,
            file_size=file_size,
            comments=comments,
            status=status
        )
        
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        return submission


@router.put("/{assignment_id}/submissions/{submission_id}/grade", response_model=SubmissionResponse)
async def grade_submission(
    assignment_id: int,
    submission_id: int,
    grade_data: SubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Grade a submission (faculty only)
    """
    submission = db.query(Submission).filter(
        Submission.id == submission_id,
        Submission.assignment_id == assignment_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Check permissions
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    course = db.query(Course).filter(Course.id == assignment.course_id).first()
    
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update grade
    if grade_data.grade is not None:
        if grade_data.grade > assignment.max_points:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Grade cannot exceed maximum points ({assignment.max_points})"
            )
        submission.grade = grade_data.grade
    
    if grade_data.feedback is not None:
        submission.feedback = grade_data.feedback
    
    if grade_data.status is not None:
        submission.status = grade_data.status
    
    submission.graded_by = current_user.id
    submission.graded_at = datetime.now()
    
    db.commit()
    db.refresh(submission)
    
    return submission
