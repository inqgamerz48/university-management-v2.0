"""
Attendance Router
Handles attendance tracking
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date, timedelta

from app.database import get_db
from app.dependencies import get_current_user, require_faculty
from app.schemas import (
    AttendanceCreate, AttendanceResponse, AttendanceBulkCreate,
    MessageResponse
)
from app.models import Attendance, Course, CourseEnrollment, User

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("/course/{course_id}", response_model=List[AttendanceResponse])
async def get_course_attendance(
    course_id: int,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Get attendance records for a course (faculty only)
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
    
    query = db.query(Attendance).filter(Attendance.course_id == course_id)
    
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)
    
    records = query.order_by(Attendance.date.desc()).all()
    return records


@router.get("/course/{course_id}/date/{attendance_date}", response_model=List[dict])
async def get_attendance_by_date(
    course_id: int,
    attendance_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Get attendance for a specific date
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get all enrolled students
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id
    ).all()
    
    # Get attendance records for this date
    records = db.query(Attendance).filter(
        Attendance.course_id == course_id,
        Attendance.date == attendance_date
    ).all()
    
    # Build response with all students
    result = []
    student_ids_with_records = {str(r.student_id) for r in records}
    
    for enrollment in enrollments:
        student = db.query(User).filter(User.id == enrollment.student_id).first()
        record = next(
            (r for r in records if str(r.student_id) == str(enrollment.student_id)),
            None
        )
        
        result.append({
            "student_id": student.id,
            "student_name": student.name,
            "student_email": student.email,
            "status": record.status if record else None,
            "notes": record.notes if record else None,
            "record_id": record.id if record else None
        })
    
    return result


@router.post("/course/{course_id}/mark", response_model=AttendanceResponse)
async def mark_attendance(
    course_id: int,
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Mark attendance for a student
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Check if record already exists
    existing = db.query(Attendance).filter(
        Attendance.course_id == course_id,
        Attendance.student_id == attendance_data.student_id,
        Attendance.date == attendance_data.date
    ).first()
    
    if existing:
        # Update existing
        existing.status = attendance_data.status
        existing.notes = attendance_data.notes
        existing.marked_by = current_user.id
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new
        attendance = Attendance(
            course_id=course_id,
            student_id=attendance_data.student_id,
            date=attendance_data.date,
            status=attendance_data.status,
            notes=attendance_data.notes,
            marked_by=current_user.id
        )
        
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance


@router.post("/course/{course_id}/mark-bulk", response_model=MessageResponse)
async def mark_attendance_bulk(
    course_id: int,
    bulk_data: AttendanceBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Mark attendance for multiple students at once
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_count = 0
    created_count = 0
    
    for record in bulk_data.records:
        student_id = UUID(record.get("student_id"))
        status = record.get("status")
        notes = record.get("notes")
        
        existing = db.query(Attendance).filter(
            Attendance.course_id == course_id,
            Attendance.student_id == student_id,
            Attendance.date == bulk_data.date
        ).first()
        
        if existing:
            existing.status = status
            existing.notes = notes
            existing.marked_by = current_user.id
            updated_count += 1
        else:
            attendance = Attendance(
                course_id=course_id,
                student_id=student_id,
                date=bulk_data.date,
                status=status,
                notes=notes,
                marked_by=current_user.id
            )
            db.add(attendance)
            created_count += 1
    
    db.commit()
    
    return {
        "message": f"Attendance saved: {created_count} new, {updated_count} updated",
        "success": True
    }


@router.get("/my-attendance", response_model=List[AttendanceResponse])
async def get_my_attendance(
    course_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's attendance records
    """
    query = db.query(Attendance).filter(Attendance.student_id == current_user.id)
    
    if course_id:
        query = query.filter(Attendance.course_id == course_id)
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)
    
    records = query.order_by(Attendance.date.desc()).all()
    return records


@router.get("/course/{course_id}/statistics", response_model=dict)
async def get_attendance_statistics(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Get attendance statistics for a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == "faculty" and str(course.faculty_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get all students
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id
    ).all()
    
    total_students = len(enrollments)
    
    # Get all attendance dates
    dates = db.query(Attendance.date).filter(
        Attendance.course_id == course_id
    ).distinct().all()
    
    total_sessions = len(dates)
    
    # Calculate statistics per student
    student_stats = []
    for enrollment in enrollments:
        student = db.query(User).filter(User.id == enrollment.student_id).first()
        records = db.query(Attendance).filter(
            Attendance.course_id == course_id,
            Attendance.student_id == enrollment.student_id
        ).all()
        
        present = sum(1 for r in records if r.status == "present")
        absent = sum(1 for r in records if r.status == "absent")
        late = sum(1 for r in records if r.status == "late")
        excused = sum(1 for r in records if r.status == "excused")
        
        attendance_rate = (present / len(records) * 100) if records else 0
        
        student_stats.append({
            "student_id": student.id,
            "student_name": student.name,
            "present": present,
            "absent": absent,
            "late": late,
            "excused": excused,
            "attendance_rate": round(attendance_rate, 2)
        })
    
    return {
        "total_students": total_students,
        "total_sessions": total_sessions,
        "student_statistics": student_stats
    }
