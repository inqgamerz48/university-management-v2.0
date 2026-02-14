"""
Dashboard Router
Handles dashboard data aggregation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas import DashboardStats, StudentDashboard, FacultyDashboard
from app.models import (
    User, Course, CourseEnrollment, Assignment, Submission,
    Notification, Attendance, Announcement
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/admin/stats", response_model=DashboardStats)
async def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get admin dashboard statistics
    """
    total_students = db.query(User).filter(User.role == "student", User.is_active == True).count()
    total_faculty = db.query(User).filter(User.role == "faculty", User.is_active == True).count()
    total_courses = db.query(Course).filter(Course.is_active == True).count()
    
    # Active assignments (due in future)
    active_assignments = db.query(Assignment).filter(
        Assignment.due_date > datetime.now(),
        Assignment.is_published == True
    ).count()
    
    # Pending submissions (submitted but not graded)
    pending_submissions = db.query(Submission).filter(
        Submission.status == "submitted"
    ).count()
    
    # Recent announcements (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_announcements = db.query(Announcement).filter(
        Announcement.created_at >= week_ago
    ).count()
    
    return {
        "total_students": total_students,
        "total_faculty": total_faculty,
        "total_courses": total_courses,
        "active_assignments": active_assignments,
        "pending_submissions": pending_submissions,
        "recent_announcements": recent_announcements
    }


@router.get("/student", response_model=dict)
async def get_student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get student dashboard data
    """
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get enrolled courses
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.student_id == current_user.id,
        CourseEnrollment.status == "active"
    ).all()
    
    enrolled_courses = []
    course_ids = []
    
    for enrollment in enrollments:
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        if course:
            course_ids.append(course.id)
            enrolled_courses.append({
                "id": course.id,
                "name": course.name,
                "code": course.code,
                "credits": course.credits,
                "faculty": course.faculty.name if course.faculty else None
            })
    
    # Get upcoming assignments
    upcoming_assignments = []
    if course_ids:
        assignments = db.query(Assignment).filter(
            Assignment.course_id.in_(course_ids),
            Assignment.due_date > datetime.now(),
            Assignment.is_published == True
        ).order_by(Assignment.due_date).limit(5).all()
        
        for assignment in assignments:
            # Check if already submitted
            submission = db.query(Submission).filter(
                Submission.assignment_id == assignment.id,
                Submission.student_id == current_user.id
            ).first()
            
            upcoming_assignments.append({
                "id": assignment.id,
                "title": assignment.title,
                "course_name": assignment.course.name if assignment.course else None,
                "due_date": assignment.due_date,
                "max_points": assignment.max_points,
                "submitted": submission is not None
            })
    
    # Get recent notifications
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    recent_notifications = [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "read": n.read,
            "created_at": n.created_at
        }
        for n in notifications
    ]
    
    # Get attendance summary
    attendance_summary = {"present": 0, "absent": 0, "late": 0, "excused": 0}
    if course_ids:
        attendance_records = db.query(Attendance).filter(
            Attendance.student_id == current_user.id,
            Attendance.course_id.in_(course_ids)
        ).all()
        
        for record in attendance_records:
            if record.status in attendance_summary:
                attendance_summary[record.status] += 1
    
    return {
        "enrolled_courses": enrolled_courses,
        "upcoming_assignments": upcoming_assignments,
        "recent_notifications": recent_notifications,
        "attendance_summary": attendance_summary
    }


@router.get("/faculty", response_model=dict)
async def get_faculty_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get faculty dashboard data
    """
    if current_user.role not in ["faculty", "admin", "super-admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get taught courses
    courses = db.query(Course).filter(
        Course.faculty_id == current_user.id,
        Course.is_active == True
    ).all()
    
    taught_courses = []
    course_ids = []
    
    for course in courses:
        course_ids.append(course.id)
        
        # Get enrollment count
        enrollment_count = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course.id,
            CourseEnrollment.status == "active"
        ).count()
        
        taught_courses.append({
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "credits": course.credits,
            "semester": course.semester,
            "year": course.year,
            "enrollment_count": enrollment_count
        })
    
    # Get pending grading count
    pending_grading = 0
    if course_ids:
        pending_grading = db.query(Submission).join(Assignment).filter(
            Assignment.course_id.in_(course_ids),
            Submission.status == "submitted"
        ).count()
    
    # Get recent submissions
    recent_submissions = []
    if course_ids:
        submissions = db.query(Submission).join(Assignment).filter(
            Assignment.course_id.in_(course_ids)
        ).order_by(Submission.submitted_at.desc()).limit(5).all()
        
        for submission in submissions:
            recent_submissions.append({
                "id": submission.id,
                "student_name": submission.student.name if submission.student else None,
                "assignment_title": submission.assignment.title if submission.assignment else None,
                "course_name": submission.assignment.course.name if submission.assignment and submission.assignment.course else None,
                "submitted_at": submission.submitted_at,
                "status": submission.status
            })
    
    # Get attendance stats
    attendance_stats = {"total_sessions": 0, "average_attendance": 0}
    if course_ids:
        # Count unique attendance dates
        dates = db.query(Attendance.date).filter(
            Attendance.course_id.in_(course_ids)
        ).distinct().count()
        
        attendance_stats["total_sessions"] = dates
    
    return {
        "taught_courses": taught_courses,
        "pending_grading": pending_grading,
        "recent_submissions": recent_submissions,
        "attendance_stats": attendance_stats
    }
