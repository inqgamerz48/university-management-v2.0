"""
Announcements Router
Handles announcements and notifications
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from app.database import get_db
from app.dependencies import get_current_user, require_faculty, require_admin
from app.schemas import (
    AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse,
    MessageResponse
)
from app.models import Announcement, Notification, User
from app.services.notification import create_notification

router = APIRouter(prefix="/announcements", tags=["Announcements"])


@router.get("/", response_model=List[AnnouncementResponse])
async def list_announcements(
    pinned_only: bool = Query(False),
    priority: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List announcements for current user
    """
    query = db.query(Announcement).filter(
        (Announcement.expires_at == None) | (Announcement.expires_at > datetime.now())
    )
    
    # Filter by user role
    query = query.filter(Announcement.target_roles.contains([current_user.role]))
    
    if pinned_only:
        query = query.filter(Announcement.is_pinned == True)
    
    if priority:
        query = query.filter(Announcement.priority == priority)
    
    announcements = query.order_by(
        Announcement.is_pinned.desc(),
        Announcement.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return announcements


@router.post("/", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Create a new announcement (faculty and admin only)
    """
    announcement = Announcement(
        **announcement_data.dict(),
        posted_by=current_user.id
    )
    
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    
    # Create notifications for target users
    # Get all users matching target roles
    target_users = db.query(User).filter(
        User.role.in_(announcement_data.target_roles),
        User.is_active == True
    ).all()
    
    for user in target_users:
        if str(user.id) != str(current_user.id):  # Don't notify self
            create_notification(
                db=db,
                user_id=user.id,
                title=f"New Announcement: {announcement_data.title}",
                message=announcement_data.content[:100] + "..." if len(announcement_data.content) > 100 else announcement_data.content,
                type="announcement",
                reference_type="announcement",
                reference_id=announcement.id,
                action_url=f"/announcements/{announcement.id}"
            )
    
    return announcement


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get announcement by ID
    """
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    # Check if user has permission to view
    if current_user.role not in announcement.target_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return announcement


@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
    announcement_id: int,
    announcement_update: AnnouncementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Update announcement (creator or admin only)
    """
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    # Check permissions
    if str(announcement.posted_by) != str(current_user.id) and current_user.role not in ["admin", "super-admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own announcements"
        )
    
    for field, value in announcement_update.dict(exclude_unset=True).items():
        setattr(announcement, field, value)
    
    db.commit()
    db.refresh(announcement)
    
    return announcement


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty)
):
    """
    Delete announcement (creator or admin only)
    """
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    if str(announcement.posted_by) != str(current_user.id) and current_user.role not in ["admin", "super-admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own announcements"
        )
    
    db.delete(announcement)
    db.commit()
    
    return None
