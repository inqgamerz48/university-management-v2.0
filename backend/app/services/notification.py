"""
Notification Service
Handles creating notifications for users
"""

from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from app.models import Notification, User


def create_notification(
    db: Session,
    user_id: UUID,
    title: str,
    message: str,
    type: str,
    reference_type: str = None,
    reference_id: int = None,
    action_url: str = None
) -> Notification:
    """
    Create a notification for a user
    """
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type,
        reference_type=reference_type,
        reference_id=reference_id,
        action_url=action_url,
        read=False
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return notification


def notify_course_students(
    db: Session,
    course_id: int,
    title: str,
    message: str,
    type: str,
    exclude_user_id: UUID = None,
    action_url: str = None
):
    """
    Create notifications for all students in a course
    """
    from app.models import CourseEnrollment
    
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id
    ).all()
    
    for enrollment in enrollments:
        if exclude_user_id and str(enrollment.student_id) == str(exclude_user_id):
            continue
        
        create_notification(
            db=db,
            user_id=enrollment.student_id,
            title=title,
            message=message,
            type=type,
            action_url=action_url
        )


def notify_new_assignment(
    db: Session,
    course_id: int,
    assignment_title: str,
    due_date: datetime = None
):
    """
    Notify students about a new assignment
    """
    message = f"New assignment posted: {assignment_title}"
    if due_date:
        message += f" (Due: {due_date.strftime('%Y-%m-%d')})"
    
    notify_course_students(
        db=db,
        course_id=course_id,
        title="New Assignment",
        message=message,
        type="assignment",
        action_url=f"/assignments"
    )


def notify_grade_posted(
    db: Session,
    student_id: UUID,
    assignment_title: str,
    grade: int,
    max_points: int
):
    """
    Notify student about a posted grade
    """
    percentage = (grade / max_points) * 100
    
    create_notification(
        db=db,
        user_id=student_id,
        title="Grade Posted",
        message=f"Your grade for '{assignment_title}' has been posted: {grade}/{max_points} ({percentage:.1f}%)",
        type="grade",
        action_url="/grades"
    )


def notify_attendance_marked(
    db: Session,
    student_id: UUID,
    course_name: str,
    date: datetime,
    status: str
):
    """
    Notify student about attendance marking
    """
    create_notification(
        db=db,
        user_id=student_id,
        title="Attendance Updated",
        message=f"Your attendance for {course_name} on {date.strftime('%Y-%m-%d')} has been marked: {status}",
        type="attendance",
        action_url="/attendance"
    )
