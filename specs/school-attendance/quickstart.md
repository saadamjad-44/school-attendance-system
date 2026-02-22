# Quickstart: School Attendance Management System

## Prerequisites

- Python 3.14 or higher
- Windows/macOS/Linux

## Setup

### 1. Clone and Install Dependencies

```bash
cd school-attendance
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 3. Access the Application

Open your browser and go to:
- Login page: http://localhost:8000/

### 4. Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | school123 |
| Principal | principal | school123 |
| Teacher | teacher1 | school123 |

## Default Sample Data

On first run, the following data is seeded:

- **1 Admin**: username: `admin`, password: `school123`
- **1 Principal**: username: `principal`, password: `school123`
- **5 Teachers**: teacher1 to teacher5, password: `school123`
- **8 Classes**: 6-A, 6-B, 7-A, 7-B, 8-A, 8-B, 9-A, 10-A
- **160 Students**: 20 students per class

## Features

### Admin
- Manage teachers (add/delete)
- Manage students (add/delete)
- Manage classes (create/assign teacher)

### Teacher
- View assigned class
- Mark daily attendance (Present/Absent/Late)
- View past 30 days history
- View notification status

### Principal
- Daily dashboard with attendance overview
- Monthly reports
- Excel download (.xlsx)
- Student-wise attendance reports
- Manage parent notifications

## Project Structure

```
├── main.py           # FastAPI application
├── database.py       # SQLite database operations
├── models.py         # Pydantic models
├── auth.py           # Authentication & sessions
├── reports.py        # Excel export
├── seed_data.py      # Sample data
├── constants.py      # App constants
├── requirements.txt  # Dependencies
├── static/           # Frontend files
│   ├── login.html
│   ├── admin.html
│   ├── teacher.html
│   ├── principal.html
│   ├── style.css
│   └── app.js
└── tests/            # Test files
```

## Running Tests

```bash
pytest tests/
```

## API Endpoints

All endpoints are available under `/api/`. See `specs/school-attendance/contracts/` for full OpenAPI spec.

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Current user

### Admin
- `GET /api/admin/teachers` - List teachers
- `POST /api/admin/teachers` - Add teacher
- `DELETE /api/admin/teachers/{id}` - Delete teacher
- `GET /api/admin/students` - List students
- `POST /api/admin/students` - Add student
- `DELETE /api/admin/students/{id}` - Delete student
- `GET /api/admin/classes` - List classes
- `POST /api/admin/classes` - Add class

### Teacher
- `GET /api/teacher/class` - Get class students
- `GET /api/teacher/attendance/today` - Today's attendance
- `POST /api/teacher/attendance` - Save attendance
- `GET /api/teacher/attendance/history` - 30-day history

### Principal
- `GET /api/principal/dashboard` - Daily summary
- `GET /api/principal/report/monthly` - Monthly data
- `GET /api/principal/report/excel` - Download Excel
- `GET /api/principal/notifications` - Pending notifications
- `POST /api/principal/notifications/{id}/send` - Mark sent
