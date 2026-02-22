# School Attendance Management System

A bilingual (Urdu + English) school attendance management system for Pakistani schools. Teachers mark daily attendance, Principals view reports and download Excel, Admins manage users and classes.

## 🌐 Live Demo

**[View Live Demo](https://school-attendance-system--saadamjad4.replit.app)** 🚀

**Demo Credentials:**
- **Admin**: username=`admin`, password=`school123`
- **Principal**: username=`principal`, password=`school123`
- **Teacher**: username=`teacher1`, password=`school123`

---

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

## Tech Stack

- **Backend**: Python 3.14+, FastAPI, Uvicorn
- **Database**: SQLite (local, no internet required)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no frameworks)
- **Authentication**: Session-based with bcrypt password hashing
- **Reports**: openpyxl for Excel export

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Seed Database (First Run)

```bash
python seed_data.py
```

This creates sample data:
- 1 Admin account
- 1 Principal account
- 5 Teachers (each assigned to a class)
- 8 Classes (6-A, 6-B, 7-A, 7-B, 8-A, 8-B, 9-A, 10-A)
- 160 Students (20 per class)

### 3. Start Server

**Option 1: Using start script (Recommended)**
```bash
# On Windows
start.bat

# On Linux/Mac
bash start.sh
```

**Option 2: Manual start**
```bash
python main.py
```

The server will start at `http://localhost:8001` (or `http://localhost:8000` if available)

### 4. Login

Open your browser and go to: `http://localhost:8001`

## Demo Credentials

All demo accounts use password: `school123`

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | school123 |
| Principal | principal | school123 |
| Teacher | teacher1 | school123 |
| Teacher | teacher2 | school123 |
| Teacher | teacher3 | school123 |
| Teacher | teacher4 | school123 |
| Teacher | teacher5 | school123 |

## Project Structure

```
├── main.py              # FastAPI application
├── database.py          # SQLite database operations
├── models.py            # Pydantic models
├── auth.py              # Authentication & sessions
├── constants.py         # App constants
├── seed_data.py         # Sample data generator
├── requirements.txt     # Python dependencies
├── school.db            # SQLite database (created on first run)
├── static/              # Frontend files
│   ├── login.html       # Login page
│   ├── admin.html       # Admin dashboard
│   ├── teacher.html     # Teacher dashboard
│   ├── principal.html   # Principal dashboard
│   ├── style.css        # Green/white theme with RTL support
│   └── app.js           # Shared JavaScript
└── specs/               # Design documents
    └── school-attendance/
        ├── spec.md      # Feature specification
        ├── plan.md      # Implementation plan
        ├── data-model.md # Database schema
        ├── quickstart.md # Setup guide
        └── tasks.md     # Task breakdown
```

## API Endpoints

### Authentication
- `POST /api/login` - Login
- `POST /api/logout` - Logout
- `GET /api/me` - Current user

### Admin
- `GET /api/admin/teachers` - List teachers
- `POST /api/admin/teachers` - Add teacher
- `DELETE /api/admin/teachers/{id}` - Delete teacher
- `GET /api/admin/students` - List students
- `POST /api/admin/students` - Add student
- `DELETE /api/admin/students/{id}` - Delete student
- `GET /api/admin/classes` - List classes
- `POST /api/admin/classes` - Add class
- `PUT /api/admin/classes/{id}/assign-teacher` - Assign teacher

### Teacher
- `GET /api/teacher/my-class` - Get assigned class students
- `GET /api/teacher/attendance/{date}` - Get attendance for date
- `POST /api/teacher/attendance` - Save attendance
- `GET /api/teacher/history` - Past 30 days history

### Principal
- `GET /api/principal/dashboard` - Daily summary
- `GET /api/principal/report` - Monthly report data
- `GET /api/principal/report/export` - Download Excel
- `GET /api/principal/student/{id}` - Student report
- `GET /api/notifications` - Pending notifications
- `POST /api/notifications/{id}/send` - Mark sent

## Database Schema

### users
- id, username, password, role, name_en, name_ur, created_at

### classes
- id, name, name_ur, teacher_id

### students
- id, name_en, name_ur, roll_no, class_id, parent_phone

### attendance
- id, student_id, class_id, date, status, marked_by, created_at

### notifications
- id, student_id, class_id, date, message, status, created_at

## Development

### Running Tests

```bash
pytest tests/
```

### Reset Database

Delete `school.db` and run `python seed_data.py` again.

## Features Implemented

✅ Admin login and authentication
✅ Teacher management (CRUD)
✅ Student management (CRUD)
✅ Class management with teacher assignment
✅ Teacher attendance marking (Present/Absent/Late)
✅ Automatic notification creation for absent students
✅ Principal daily dashboard with stats
✅ Monthly attendance reports
✅ Excel export (.xlsx)
✅ Student-wise attendance history
✅ Teacher class history (30 days)
✅ Sample data seeding
✅ Bilingual UI (Urdu + English)
✅ Mobile responsive design
✅ Role-based access control

## License

MIT

## Support

For issues or questions, please refer to the documentation in `specs/school-attendance/`.
