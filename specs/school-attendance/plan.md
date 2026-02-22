# Implementation Plan: School Attendance Management System

**Branch**: `main` | **Date**: 2026-02-22 | **Spec**: [specs/school-attendance/spec.md](./spec.md)

## Summary

A bilingual (Urdu + English) school attendance management system for Pakistani schools. Teachers mark daily attendance (Present/Absent/Late), Principals view reports and download Excel, Admins manage users and classes. Fully local SQLite database with session-based authentication.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: FastAPI, Uvicorn, openpyxl, bcrypt, python-multipart, fastapi-sessions
**Storage**: SQLite (file: `school.db`)
**Testing**: pytest, httpx
**Target Platform**: Web browser (responsive, mobile-friendly)
**Project Type**: Web application (single backend + static frontend)
**Performance Goals**: <2s page load, <5s Excel export
**Constraints**: Fully offline-capable, no internet required
**Scale/Scope**: ~200 students, 8 classes, ~10 users

## Constitution Check

| Constraint | Status |
|------------|--------|
| Python 3.14+ | ✅ Using Python 3.14+ |
| FastAPI + Uvicorn | ✅ FastAPI for API, Uvicorn for server |
| SQLite only | ✅ Using sqlite3 (built-in) |
| Plain HTML/CSS/JS | ✅ Vanilla frontend, no frameworks |
| Session-based auth | ✅ FastAPI sessions |
| openpyxl for Excel | ✅ Required for reports |
| pytest + httpx | ✅ Testing framework |
| No SQLAlchemy | ✅ Using raw sqlite3 |
| No Bootstrap | ✅ Custom CSS |
| Type hints | ✅ All functions typed |
| English comments | ✅ Required |
| Constants in constants.py | ✅ Required |

**GATE PASSED**: All constitution constraints satisfied.

## Project Structure

### Documentation (this feature)

```
specs/school-attendance/
├── plan.md              # This file
├── spec.md             # Feature specification
├── data-model.md       # Phase 1 output (entities, relationships)
├── quickstart.md       # Phase 1 output (setup instructions)
└── contracts/          # Phase 1 output (API endpoints)
```

### Source Code (repository root)

```
├── main.py              # FastAPI app, routes, auth middleware
├── database.py          # SQLite connection and queries
├── models.py            # Pydantic models
├── auth.py              # Login, logout, session, password hash
├── reports.py           # Excel export logic
├── seed_data.py         # Sample school data
├── constants.py         # All constants
├── requirements.txt     # Dependencies
├── static/
│   ├── login.html       # Login page
│   ├── teacher.html     # Teacher dashboard
│   ├── principal.html   # Principal dashboard
│   ├── admin.html       # Admin panel
│   ├── style.css        # Green/white school theme, RTL support
│   └── app.js           # Shared JavaScript
└── tests/
    ├── test_auth.py
    ├── test_attendance.py
    └── test_reports.py
```

**Structure Decision**: Single FastAPI backend serving static HTML files. Simple, no build step required.

## API Endpoints (Contracts)

### Auth
- `POST /api/auth/login` - Login with username/password
- `POST /api/auth/logout` - Logout current session
- `GET /api/auth/me` - Get current user info

### Admin
- `GET /api/admin/teachers` - List all teachers
- `POST /api/admin/teachers` - Create teacher
- `DELETE /api/admin/teachers/{id}` - Delete teacher
- `GET /api/admin/students` - List students (filter by class)
- `POST /api/admin/students` - Create student
- `DELETE /api/admin/students/{id}` - Delete student
- `GET /api/admin/classes` - List all classes
- `POST /api/admin/classes` - Create class
- `PUT /api/admin/classes/{id}/assign-teacher` - Assign teacher to class

### Teacher
- `GET /api/teacher/class` - Get assigned class students
- `GET /api/teacher/attendance/today` - Get today's attendance
- `POST /api/teacher/attendance` - Save/update attendance
- `GET /api/teacher/attendance/history` - Past 30 days history
- `GET /api/teacher/notifications` - Get notifications sent

### Principal
- `GET /api/principal/dashboard` - Daily attendance summary
- `GET /api/principal/report/monthly` - Monthly report data
- `GET /api/principal/report/excel` - Download Excel file
- `GET /api/principal/report/student/{id}` - Student-wise report
- `GET /api/principal/notifications` - All pending notifications
- `POST /api/principal/notifications/{id}/send` - Mark as sent

### Pages Served (Static HTML)
- `GET /` - Redirect to login
- `GET /login` - login.html
- `GET /teacher` - teacher.html (auth required)
- `GET /principal` - principal.html (auth required)
- `GET /admin` - admin.html (auth required)

## Data Model

### users
| Field | Type | Constraints |
|-------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| username | TEXT | UNIQUE NOT NULL |
| password | TEXT | NOT NULL (bcrypt hashed) |
| role | TEXT | NOT NULL ('admin','teacher','principal') |
| name_en | TEXT | NOT NULL |
| name_ur | TEXT | NULLABLE |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

### classes
| Field | Type | Constraints |
|-------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL (e.g. 'Class 8-A') |
| name_ur | TEXT | NULLABLE (e.g. 'جماعت ہشتم الف') |
| teacher_id | INTEGER | REFERENCES users(id) |

### students
| Field | Type | Constraints |
|-------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| name_en | TEXT | NOT NULL |
| name_ur | TEXT | NULLABLE |
| roll_no | TEXT | NOT NULL |
| class_id | INTEGER | REFERENCES classes(id) |
| parent_phone | TEXT | NULLABLE |

### attendance
| Field | Type | Constraints |
|-------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| student_id | INTEGER | REFERENCES students(id) |
| class_id | INTEGER | REFERENCES classes(id) |
| date | TEXT | NOT NULL (YYYY-MM-DD) |
| status | TEXT | NOT NULL ('present','absent','late') |
| marked_by | INTEGER | REFERENCES users(id) |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |
| UNIQUE | (student_id, date) | |

### notifications
| Field | Type | Constraints |
|-------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| student_id | INTEGER | REFERENCES students(id) |
| date | TEXT | NOT NULL |
| message | TEXT | NULLABLE |
| status | TEXT | DEFAULT 'pending' ('pending','sent') |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

## Excel Export Format
Sheet: Monthly Attendance Report
Columns: Roll No | Student Name | 1 | 2 | ... 31 | Total P | Total A | %
Legend: P = Present, A = Absent, L = Late

## Run Instructions
```bash
pip install -r requirements.txt
uvicorn main:app --reload
# Open http://localhost:8000
```

## Default Logins (Seed Data)
| Role | Username | Password | Class |
|------|-----------|----------|-------|
| Admin | admin | school123 | - |
| Principal | principal | school123 | - |
| Teacher | teacher1 | school123 | Class 6-A |
| Teacher | teacher2 | school123 | Class 7-A |

## Phase 1 Output Files

1. **data-model.md** - This section expanded into detailed schema
2. **quickstart.md** - Setup instructions for developers
3. **contracts/** - OpenAPI spec for all endpoints
