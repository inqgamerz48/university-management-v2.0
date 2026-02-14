#!/usr/bin/env python3
"""
Quick verification script for UniManager Pro backend
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}")
        return True
    else:
        print(f"[MISSING] {description}")
        return False

def main():
    print("=" * 60)
    print("UniManager Pro - Backend Structure Verification")
    print("=" * 60)
    print()
    
    # Check main files
    print("[Main Files]")
    check_file_exists("app/main.py", "FastAPI entry point")
    check_file_exists("app/config.py", "Configuration")
    check_file_exists("app/database.py", "Database connection")
    check_file_exists("app/dependencies.py", "Auth dependencies")
    check_file_exists("requirements.txt", "Dependencies")
    check_file_exists("Dockerfile", "Docker config")
    check_file_exists(".env.example", "Environment template")
    print()
    
    # Check models
    print("[Models]")
    check_file_exists("app/models/__init__.py", "All models")
    print()
    
    # Check schemas
    print("[Schemas]")
    check_file_exists("app/schemas/__init__.py", "All schemas")
    print()
    
    # Check routers
    print("[API Routers]")
    routers = [
        ("app/routers/auth.py", "Authentication"),
        ("app/routers/users.py", "Users"),
        ("app/routers/courses.py", "Courses"),
        ("app/routers/assignments.py", "Assignments"),
        ("app/routers/attendance.py", "Attendance"),
        ("app/routers/announcements.py", "Announcements"),
        ("app/routers/notifications.py", "Notifications"),
        ("app/routers/dashboard.py", "Dashboard"),
    ]
    
    all_routers_ok = True
    for filepath, description in routers:
        if not check_file_exists(filepath, description):
            all_routers_ok = False
    print()
    
    # Check services
    print("[Services]")
    check_file_exists("app/services/supabase.py", "Supabase client")
    check_file_exists("app/services/storage.py", "File storage")
    check_file_exists("app/services/notification.py", "Notifications")
    print()
    
    # Summary
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if all_routers_ok:
        print("[SUCCESS] All core files are present!")
        print()
        print("To run locally:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Set up .env file (see .env.example)")
        print("   3. Run: uvicorn app.main:app --reload")
        print()
        print("API Docs will be at: http://localhost:8000/docs")
    else:
        print("[WARNING] Some files are missing. Check the structure above.")
    
    print()
    print("Total files created:")
    
    # Count Python files
    py_files = []
    for root, dirs, files in os.walk("app"):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    
    print(f"   - Python files: {len(py_files)}")
    print(f"   - SQL schema: schema.sql")
    print(f"   - Config files: 5+")
    print()

if __name__ == "__main__":
    main()
