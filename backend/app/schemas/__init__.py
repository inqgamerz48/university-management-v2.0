"""
Pydantic Schemas for request/response validation
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


# ============== User Schemas ==============

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str = Field(..., pattern="^(student|faculty|admin|super-admin)$")
    department: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ============== Department Schemas ==============

class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    head_id: Optional[UUID] = None


class DepartmentResponse(DepartmentBase):
    id: int
    head_id: Optional[UUID]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Course Schemas ==============

class CourseBase(BaseModel):
    name: str
    code: str
    credits: int = 3
    description: Optional[str] = None
    semester: Optional[str] = None
    year: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class CourseCreate(CourseBase):
    department_id: Optional[int] = None
    faculty_id: Optional[UUID] = None


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    credits: Optional[int] = None
    description: Optional[str] = None
    semester: Optional[str] = None
    year: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    faculty_id: Optional[UUID] = None


class CourseResponse(CourseBase):
    id: int
    department_id: Optional[int]
    faculty_id: Optional[UUID]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CourseWithDetails(CourseResponse):
    department: Optional[DepartmentResponse] = None
    faculty: Optional[UserResponse] = None
    enrolled_count: int = 0


# ============== Enrollment Schemas ==============

class EnrollmentCreate(BaseModel):
    course_id: int
    student_id: UUID


class EnrollmentResponse(BaseModel):
    id: int
    course_id: int
    student_id: UUID
    enrolled_at: datetime
    status: str
    
    class Config:
        from_attributes = True


# ============== Assignment Schemas ==============

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    due_date: Optional[datetime] = None
    max_points: int = 100
    allow_late_submission: bool = False
    late_penalty_percent: int = 0


class AssignmentCreate(AssignmentBase):
    course_id: int


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    due_date: Optional[datetime] = None
    max_points: Optional[int] = None
    allow_late_submission: Optional[bool] = None
    late_penalty_percent: Optional[int] = None
    is_published: Optional[bool] = None


class AssignmentResponse(AssignmentBase):
    id: int
    course_id: int
    file_url: Optional[str]
    created_by: Optional[UUID]
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssignmentWithCourse(AssignmentResponse):
    course: Optional[CourseResponse] = None


# ============== Submission Schemas ==============

class SubmissionBase(BaseModel):
    comments: Optional[str] = None


class SubmissionCreate(SubmissionBase):
    assignment_id: int


class SubmissionUpdate(BaseModel):
    grade: Optional[int] = None
    feedback: Optional[str] = None
    status: Optional[str] = None


class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: UUID
    file_url: Optional[str]
    file_name: Optional[str]
    file_size: Optional[int]
    comments: Optional[str]
    submitted_at: datetime
    status: str
    grade: Optional[int]
    feedback: Optional[str]
    graded_by: Optional[UUID]
    graded_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class SubmissionWithDetails(SubmissionResponse):
    assignment: Optional[AssignmentResponse] = None
    student: Optional[UserResponse] = None


# ============== Attendance Schemas ==============

class AttendanceBase(BaseModel):
    status: str = Field(..., pattern="^(present|absent|late|excused)$")
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    course_id: int
    student_id: UUID
    date: date


class AttendanceBulkCreate(BaseModel):
    course_id: int
    date: date
    records: List[dict]  # [{"student_id": "uuid", "status": "present"}]


class AttendanceResponse(BaseModel):
    id: int
    course_id: int
    student_id: UUID
    date: date
    status: str
    notes: Optional[str]
    marked_by: Optional[UUID]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Announcement Schemas ==============

class AnnouncementBase(BaseModel):
    title: str
    content: str
    target_roles: List[str] = ["student", "faculty", "admin"]
    target_departments: Optional[List[int]] = None
    target_courses: Optional[List[int]] = None
    priority: str = "normal"
    is_pinned: bool = False


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    is_pinned: Optional[bool] = None
    expires_at: Optional[datetime] = None


class AnnouncementResponse(AnnouncementBase):
    id: int
    posted_by: Optional[UUID]
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============== Notification Schemas ==============

class NotificationBase(BaseModel):
    title: str
    message: str
    type: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    action_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    user_id: UUID


class NotificationResponse(NotificationBase):
    id: int
    user_id: UUID
    read: bool
    read_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class NotificationMarkRead(BaseModel):
    notification_ids: List[int]


# ============== Grade Schemas ==============

class GradeBase(BaseModel):
    grade_type: str
    points: int
    max_points: int
    comments: Optional[str] = None


class GradeCreate(GradeBase):
    student_id: UUID
    course_id: int
    assignment_id: Optional[int] = None


class GradeResponse(GradeBase):
    id: int
    student_id: UUID
    course_id: int
    assignment_id: Optional[int]
    percentage: Optional[float]
    letter_grade: Optional[str]
    graded_by: Optional[UUID]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Support Ticket Schemas ==============

class SupportTicketBase(BaseModel):
    subject: str
    description: str
    category: str
    priority: str = "medium"


class SupportTicketCreate(SupportTicketBase):
    pass


class SupportTicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[UUID] = None
    resolution_notes: Optional[str] = None


class SupportTicketResponse(SupportTicketBase):
    id: int
    user_id: UUID
    status: str
    assigned_to: Optional[UUID]
    resolution_notes: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Dashboard Schemas ==============

class DashboardStats(BaseModel):
    total_students: int
    total_faculty: int
    total_courses: int
    active_assignments: int
    pending_submissions: int
    recent_announcements: int


class StudentDashboard(BaseModel):
    enrolled_courses: List[CourseResponse]
    upcoming_assignments: List[AssignmentResponse]
    recent_notifications: List[NotificationResponse]
    attendance_summary: dict


class FacultyDashboard(BaseModel):
    taught_courses: List[CourseWithDetails]
    pending_grading: int
    recent_submissions: List[SubmissionResponse]
    attendance_stats: dict


# ============== File Upload Schemas ==============

class FileUploadResponse(BaseModel):
    url: str
    file_name: str
    file_size: int
    file_type: str


class PresignedUrlResponse(BaseModel):
    url: str
    fields: Optional[dict] = None


# ============== Auth Schemas ==============

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


# ============== Generic Response Schemas ==============

class MessageResponse(BaseModel):
    message: str
    success: bool = True


class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int
