"""
File Storage Service
Handles file uploads to Supabase Storage
"""

import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException

from app.services.supabase import get_supabase_admin_client
from app.config import get_settings

settings = get_settings()


async def upload_file_to_storage(
    file: UploadFile,
    folder: str = "",
    user_id: Optional[str] = None,
    allowed_extensions: list = None
) -> dict:
    """
    Upload a file to Supabase Storage
    
    Returns:
        dict: {url, file_name, file_size, file_type}
    """
    if allowed_extensions is None:
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.zip', '.jpg', '.png']
    
    # Validate file size
    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Validate file extension
    file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
    if f'.{file_ext}' not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = f"{unique_id}_{file.filename}"
    
    if folder:
        path = f"{folder}/{safe_filename}"
    else:
        path = safe_filename
    
    try:
        supabase = get_supabase_admin_client()
        
        # Upload to Supabase Storage
        result = supabase.storage.from_(settings.STORAGE_BUCKET).upload(
            path=path,
            file=contents,
            file_options={"content-type": file.content_type}
        )
        
        # Get public URL
        url = supabase.storage.from_(settings.STORAGE_BUCKET).get_public_url(path)
        
        return {
            "url": url,
            "file_name": file.filename,
            "file_size": len(contents),
            "file_type": file.content_type,
            "path": path
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )


async def delete_file_from_storage(file_path: str) -> bool:
    """
    Delete a file from Supabase Storage
    """
    try:
        supabase = get_supabase_admin_client()
        supabase.storage.from_(settings.STORAGE_BUCKET).remove([file_path])
        return True
    except Exception as e:
        return False


async def get_presigned_upload_url(
    file_name: str,
    folder: str = "",
    expiry_seconds: int = 300
) -> dict:
    """
    Get a presigned URL for direct client-side upload
    """
    try:
        supabase = get_supabase_admin_client()
        
        if folder:
            path = f"{folder}/{file_name}"
        else:
            path = file_name
        
        # Create signed upload URL
        result = supabase.storage.from_(settings.STORAGE_BUCKET).create_signed_upload_url(
            path=path
        )
        
        return {
            "url": result["signedURL"],
            "token": result["token"],
            "path": path
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create upload URL: {str(e)}"
        )
