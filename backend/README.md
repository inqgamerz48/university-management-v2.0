# UniManager Pro - Backend

A production-ready FastAPI backend for the UniManager Pro university management system.

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: Supabase Auth (JWT)
- **File Storage**: Supabase Storage
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection & session
│   ├── dependencies.py      # Auth dependencies
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   └── services/            # Business logic
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── Dockerfile
├── requirements.txt
├── schema.sql              # Database schema
└── .env.example
```

## Quick Start

### 1. Environment Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Run the SQL schema in your Supabase SQL Editor:
```sql
-- Copy contents of schema.sql
```

Or use Alembic migrations:
```bash
alembic upgrade head
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000/api/v1
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/unimanager

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=UniManager Pro API
DEBUG=true
SECRET_KEY=your-secret-key

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Storage
STORAGE_BUCKET=unimanager-files
MAX_FILE_SIZE=10485760
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Get current user

### Users
- `GET /api/v1/users/` - List users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `GET /api/v1/users/{id}/courses` - Get user's courses

### Courses
- `GET /api/v1/courses/` - List courses
- `POST /api/v1/courses/` - Create course
- `GET /api/v1/courses/{id}` - Get course by ID
- `PUT /api/v1/courses/{id}` - Update course
- `DELETE /api/v1/courses/{id}` - Delete course
- `GET /api/v1/courses/{id}/enrollments` - Get course enrollments
- `POST /api/v1/courses/{id}/enroll` - Enroll student

### Assignments
- `GET /api/v1/assignments/` - List assignments
- `POST /api/v1/assignments/` - Create assignment
- `GET /api/v1/assignments/{id}` - Get assignment
- `PUT /api/v1/assignments/{id}` - Update assignment
- `DELETE /api/v1/assignments/{id}` - Delete assignment
- `POST /api/v1/assignments/{id}/submit` - Submit assignment
- `GET /api/v1/assignments/{id}/my-submission` - Get my submission
- `PUT /api/v1/assignments/{id}/submissions/{sub_id}/grade` - Grade submission

### Attendance
- `GET /api/v1/attendance/course/{id}` - Get course attendance
- `POST /api/v1/attendance/course/{id}/mark` - Mark attendance
- `POST /api/v1/attendance/course/{id}/mark-bulk` - Bulk mark attendance
- `GET /api/v1/attendance/my-attendance` - Get my attendance

### Announcements
- `GET /api/v1/announcements/` - List announcements
- `POST /api/v1/announcements/` - Create announcement
- `GET /api/v1/announcements/{id}` - Get announcement
- `PUT /api/v1/announcements/{id}` - Update announcement
- `DELETE /api/v1/announcements/{id}` - Delete announcement

### Notifications
- `GET /api/v1/notifications/` - Get notifications
- `GET /api/v1/notifications/unread-count` - Get unread count
- `POST /api/v1/notifications/{id}/mark-read` - Mark as read
- `POST /api/v1/notifications/mark-all-read` - Mark all as read

### Dashboard
- `GET /api/v1/dashboard/admin/stats` - Admin stats
- `GET /api/v1/dashboard/student` - Student dashboard
- `GET /api/v1/dashboard/faculty` - Faculty dashboard

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <supabase-jwt-token>
```

## Deployment

### Docker

```bash
docker build -t unimanager-backend .
docker run -p 8000:8000 --env-file .env unimanager-backend
```

### Production Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=false`
- [ ] Configure CORS origins for production domain
- [ ] Set up SSL/TLS
- [ ] Configure database connection pooling
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback one migration:
```bash
alembic downgrade -1
```

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## License

MIT
