# 🎓 UniManager Pro

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js" alt="Next.js">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-14+-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase" alt="Supabase">
  <img src="https://img.shields.io/badge/Tailwind-38B2AC?style=for-the-badge&logo=tailwind-css" alt="Tailwind">
</p>

<p align="center">
  <strong>A modern, full-stack university management system</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#deployment">Deployment</a> •
  <a href="#api-documentation">API</a>
</p>

---

## ✨ Features

### 🔐 Authentication & Authorization
- **Supabase Auth** integration with JWT tokens
- Role-based access control (RBAC)
- Four user roles: Student, Faculty, Admin, Super Admin
- Secure password reset and email verification

### 📚 Course Management
- Create and manage courses with departments
- Student enrollment system
- Faculty assignment
- Course scheduling (semester, year, dates)

### 📝 Assignment System
- Create assignments with due dates
- File upload support (PDF, DOC, images)
- Submission tracking
- Late submission handling with penalties
- Grade management with feedback

### 📊 Attendance Tracking
- Mark attendance for students
- Bulk attendance marking
- Attendance statistics and reports
- Present/Absent/Late/Excused status

### 📢 Announcements & Notifications
- Role-targeted announcements
- Real-time notifications
- Priority levels (Low, Normal, High, Urgent)
- Pinned announcements

### 📈 Dashboards
- **Admin Dashboard**: System overview, user management, statistics
- **Faculty Dashboard**: Courses taught, pending grading, submissions
- **Student Dashboard**: Enrolled courses, upcoming assignments, notifications

### 🎨 UI/UX
- Modern dark theme with gold accents
- Glass-morphism design
- Responsive layout (mobile, tablet, desktop)
- Smooth animations and transitions
- Accessible components (shadcn/ui)

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State**: React Context + Hooks
- **Icons**: Lucide React
- **Charts**: Recharts

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: Supabase Auth (JWT)
- **Validation**: Pydantic
- **File Storage**: Supabase Storage

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Render
- **Database**: Supabase PostgreSQL
- **Auth**: Supabase Auth
- **Storage**: Supabase Storage

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database (or Supabase account)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/inqgamerz48/university-management-v2.0.git
cd university-management-v2.0
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your Supabase credentials

# Run server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local with your credentials

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:9002`

---

## 📋 Environment Variables

### Backend (.env)

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
SECRET_KEY=your-secret-key
DEBUG=true
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:9002"]

# Storage
STORAGE_BUCKET=unimanager-files
MAX_FILE_SIZE=10485760
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 🌐 Deployment

### Deploy to Vercel (Frontend)

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Add environment variables
5. Deploy!

### Deploy to Render (Backend)

1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables
5. Deploy!

### Supabase Setup

1. Create project at [supabase.com](https://supabase.com)
2. Run the SQL schema from `backend/schema.sql`
3. Enable Storage bucket
4. Copy credentials to environment variables

---

## 📚 API Documentation

### Authentication Endpoints

```http
POST   /api/v1/auth/signup          # Register new user
POST   /api/v1/auth/login           # Login user
POST   /api/v1/auth/logout          # Logout user
POST   /api/v1/auth/refresh         # Refresh token
GET    /api/v1/auth/me              # Get current user
```

### Users

```http
GET    /api/v1/users/               # List users
GET    /api/v1/users/{id}           # Get user by ID
PUT    /api/v1/users/{id}           # Update user
DELETE /api/v1/users/{id}           # Delete user
GET    /api/v1/users/{id}/courses   # Get user's courses
```

### Courses

```http
GET    /api/v1/courses/             # List courses
POST   /api/v1/courses/             # Create course
GET    /api/v1/courses/{id}         # Get course
PUT    /api/v1/courses/{id}         # Update course
DELETE /api/v1/courses/{id}         # Delete course
POST   /api/v1/courses/{id}/enroll  # Enroll student
```

### Assignments

```http
GET    /api/v1/assignments/         # List assignments
POST   /api/v1/assignments/         # Create assignment
GET    /api/v1/assignments/{id}     # Get assignment
PUT    /api/v1/assignments/{id}     # Update assignment
DELETE /api/v1/assignments/{id}     # Delete assignment
POST   /api/v1/assignments/{id}/submit              # Submit
PUT    /api/v1/assignments/{id}/submissions/{sid}/grade  # Grade
```

### Attendance

```http
GET    /api/v1/attendance/course/{id}      # Get course attendance
POST   /api/v1/attendance/course/{id}/mark # Mark attendance
POST   /api/v1/attendance/course/{id}/mark-bulk  # Bulk mark
GET    /api/v1/attendance/my-attendance    # Get my attendance
```

### Dashboard

```http
GET    /api/v1/dashboard/admin/stats   # Admin statistics
GET    /api/v1/dashboard/student       # Student dashboard
GET    /api/v1/dashboard/faculty       # Faculty dashboard
```

---

## 🏗️ Project Structure

```
university-management-v2.0/
├── frontend/                    # Next.js Frontend
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   ├── components/         # React Components
│   │   ├── context/            # Auth Context
│   │   ├── lib/                # Utilities & API
│   │   └── hooks/              # Custom Hooks
│   ├── public/                 # Static Assets
│   └── package.json
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── routers/            # API Routes
│   │   ├── models/             # Database Models
│   │   ├── schemas/            # Pydantic Schemas
│   │   ├── services/           # Business Logic
│   │   ├── main.py             # Entry Point
│   │   └── config.py           # Configuration
│   ├── schema.sql              # Database Schema
│   ├── requirements.txt        # Python Dependencies
│   └── Dockerfile
│
└── docs/                        # Documentation
    ├── DEPLOYMENT_GUIDE.md
    └── IMPLEMENTATION_GUIDE.md
```

---

## 🎯 Features by Role

### 👨‍🎓 Student
- View enrolled courses
- Submit assignments with file uploads
- Check grades and feedback
- View attendance records
- Receive notifications
- Access course materials

### 👨‍🏫 Faculty
- Manage taught courses
- Create assignments
- Grade submissions
- Mark attendance
- Post announcements
- View student progress

### 👨‍💼 Admin
- User management
- Course management
- System statistics
- Bulk operations
- Support ticket handling
- System configuration

---

## 🔒 Security Features

- ✅ JWT Authentication via Supabase
- ✅ Role-based Access Control (RBAC)
- ✅ Row Level Security (RLS) in PostgreSQL
- ✅ Input validation with Pydantic
- ✅ SQL Injection protection via SQLAlchemy ORM
- ✅ CORS configuration
- ✅ File upload security (size limits, type validation)
- ✅ Password hashing (bcrypt)
- ✅ Secure HTTP headers

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 🛣️ Roadmap

- [ ] Real-time notifications via WebSockets
- [ ] Mobile app (React Native)
- [ ] Calendar integration
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Dark/Light theme toggle
- [ ] Offline mode support

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for beautiful components
- [Supabase](https://supabase.com/) for backend infrastructure
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing Python framework
- [Next.js](https://nextjs.org/) for the React framework
- [Tailwind CSS](https://tailwindcss.com/) for styling

---

## 📞 Support

Having issues? 
- Check the [Deployment Guide](DEPLOYMENT_GUIDE.md)
- Check the [Implementation Guide](IMPLEMENTATION_GUIDE.md)
- Open an issue on GitHub

---

<p align="center">
  Made with ❤️ for better education management
</p>

<p align="center">
  <a href="https://github.com/inqgamerz48/university-management-v2.0">⭐ Star this repo</a>
</p>
