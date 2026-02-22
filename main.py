# Main FastAPI application for School Attendance System

import os
from datetime import date, timedelta
from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from constants import (
    ROLE_ADMIN, ROLE_PRINCIPAL, ROLE_TEACHER,
    STATUS_PRESENT, STATUS_ABSENT, STATUS_LATE,
    NOTIFICATION_PENDING, NOTIFICATION_SENT,
    SESSION_COOKIE_NAME, MSG_INVALID_CREDENTIALS
)
from database import init_db, execute_query, execute_insert, execute_update, rows_to_list, row_to_dict
from auth import authenticate_user, get_user_from_session, create_session, delete_session, get_user_by_id
from models import (
    LoginRequest, UserResponse, TeacherCreate, StudentCreate, ClassCreate,
    AssignTeacherRequest, AttendanceSaveRequest, DashboardStats, DashboardResponse,
    ClassSummary, MonthlyReportResponse, MonthlyReportStudent, NotificationResponse
)

# Initialize database on startup
init_db()

app = FastAPI(title="School Attendance System")

# Add CORS middleware to allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple session dependency
def get_current_user(request: Request) -> Optional[dict]:
    """Get current user from session cookie."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id:
        return get_user_from_session(session_id)
    return None


def require_role(allowed_roles: list[str]):
    """Dependency to require specific roles."""
    def role_checker(user: Optional[dict] = Depends(get_current_user)) -> dict:
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if user['role'] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return role_checker


# ==================== AUTH ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to login or dashboard based on auth status."""
    user = get_current_user(request)
    if user:
        if user['role'] == ROLE_ADMIN:
            return HTMLResponse(content="", headers={"Location": "/admin"})
        elif user['role'] == ROLE_PRINCIPAL:
            return HTMLResponse(content="", headers={"Location": "/principal"})
        elif user['role'] == ROLE_TEACHER:
            return HTMLResponse(content="", headers={"Location": "/teacher"})
    return HTMLResponse(content="", headers={"Location": "/login"})


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """Serve login page."""
    with open("static/login.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/login")
async def login(request: Request, login_data: LoginRequest):
    """Login endpoint."""
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail=MSG_INVALID_CREDENTIALS)

    # Create session
    session_id = create_session(user['id'])

    response = JSONResponse(content=UserResponse(
        id=user['id'],
        username=user['username'],
        name_en=user['name_en'],
        name_ur=user.get('name_ur'),
        role=user['role']
    ).model_dump())

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        samesite="lax"
    )
    return response


@app.post("/api/logout")
async def logout(request: Request):
    """Logout endpoint."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id:
        delete_session(session_id)

    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


@app.get("/api/me")
async def get_me(user: Optional[dict] = Depends(get_current_user)):
    """Get current user."""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UserResponse(
        id=user['id'],
        username=user['username'],
        name_en=user['name_en'],
        name_ur=user.get('name_ur'),
        role=user['role']
    )


# ==================== ADMIN ROUTES ====================

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Serve admin page."""
    with open("static/admin.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/admin/teachers")
async def get_teachers(user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Get all teachers."""
    rows = execute_query("""
        SELECT u.id, u.username, u.name_en, u.name_ur, c.id as class_id, c.name as class_name
        FROM users u
        LEFT JOIN classes c ON u.id = c.teacher_id
        WHERE u.role = 'teacher'
        ORDER BY u.name_en
    """)
    return rows_to_list(rows)


@app.post("/api/admin/teachers")
async def create_teacher(teacher: TeacherCreate, user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Create a new teacher."""
    from auth import create_user, hash_password

    hashed = hash_password(teacher.password)
    user_id = execute_insert(
        "INSERT INTO users (username, password, role, name_en, name_ur) VALUES (?, ?, ?, ?, ?)",
        (teacher.username, hashed, ROLE_TEACHER, teacher.name_en, teacher.name_ur)
    )

    # Assign to class if specified
    if teacher.class_id:
        execute_update("UPDATE classes SET teacher_id = ? WHERE id = ?", (user_id, teacher.class_id))

    return {"id": user_id, "message": "Teacher created"}


@app.delete("/api/admin/teachers/{teacher_id}")
async def delete_teacher(teacher_id: int, user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Delete a teacher."""
    execute_update("DELETE FROM users WHERE id = ? AND role = 'teacher'", (teacher_id,))
    return {"message": "Teacher deleted"}


@app.get("/api/admin/students")
async def get_students(class_id: Optional[int] = None, user: dict = Depends(require_role([ROLE_ADMIN, ROLE_PRINCIPAL]))):
    """Get students, optionally filtered by class."""
    if class_id:
        rows = execute_query(
            "SELECT * FROM students WHERE class_id = ? ORDER BY roll_no",
            (class_id,)
        )
    else:
        rows = execute_query("SELECT * FROM students ORDER BY class_id, roll_no")
    return rows_to_list(rows)


@app.post("/api/admin/students")
async def create_student(student: StudentCreate, user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Create a new student."""
    student_id = execute_insert(
        "INSERT INTO students (name_en, name_ur, roll_no, class_id, parent_phone) VALUES (?, ?, ?, ?, ?)",
        (student.name_en, student.name_ur, student.roll_no, student.class_id, student.parent_phone)
    )
    return {"id": student_id, "message": "Student created"}


@app.delete("/api/admin/students/{student_id}")
async def delete_student(student_id: int, user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Delete a student."""
    execute_update("DELETE FROM students WHERE id = ?", (student_id,))
    return {"message": "Student deleted"}


@app.get("/api/admin/classes")
async def get_classes(user: dict = Depends(require_role([ROLE_ADMIN, ROLE_PRINCIPAL]))):
    """Get all classes."""
    rows = execute_query("""
        SELECT c.*, u.name_en as teacher_name
        FROM classes c
        LEFT JOIN users u ON c.teacher_id = u.id
        ORDER BY c.name
    """)
    return rows_to_list(rows)


@app.post("/api/admin/classes")
async def create_class(class_data: ClassCreate, user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Create a new class."""
    class_id = execute_insert(
        "INSERT INTO classes (name, name_ur) VALUES (?, ?)",
        (class_data.name, class_data.name_ur)
    )
    return {"id": class_id, "message": "Class created"}


@app.put("/api/admin/classes/{class_id}/assign-teacher")
async def assign_teacher(class_id: int, data: AssignTeacherRequest, user: dict = Depends(require_role([ROLE_ADMIN]))):
    """Assign a teacher to a class."""
    if data.teacher_id:
        execute_update("UPDATE classes SET teacher_id = ? WHERE id = ?", (data.teacher_id, class_id))
    else:
        execute_update("UPDATE classes SET teacher_id = NULL WHERE id = ?", (class_id,))
    return {"message": "Teacher assigned"}


# ==================== TEACHER ROUTES ====================

@app.get("/teacher", response_class=HTMLResponse)
async def teacher_page(user: dict = Depends(require_role([ROLE_TEACHER]))):
    """Serve teacher page."""
    with open("static/teacher.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/teacher/my-class")
async def get_my_class(user: dict = Depends(require_role([ROLE_TEACHER]))):
    """Get teacher's assigned class with students."""
    # Get class for this teacher
    class_rows = execute_query(
        "SELECT * FROM classes WHERE teacher_id = ?",
        (user['id'],)
    )
    if not class_rows:
        return {"class": None, "students": []}

    class_data = row_to_dict(class_rows[0])

    # Get students for this class
    student_rows = execute_query(
        "SELECT * FROM students WHERE class_id = ? ORDER BY roll_no",
        (class_data['id'],)
    )
    students = rows_to_list(student_rows)

    # Get today's attendance
    today = date.today().isoformat()
    attendance_rows = execute_query(
        "SELECT student_id, status FROM attendance WHERE class_id = ? AND date = ?",
        (class_data['id'], today)
    )
    attendance_map = {row['student_id']: row['status'] for row in attendance_rows}

    # Add status to students
    for student in students:
        student['status'] = attendance_map.get(student['id'], STATUS_PRESENT)

    return {"class": class_data, "students": students}


@app.get("/api/teacher/attendance/{attendance_date}")
async def get_attendance(attendance_date: str, user: dict = Depends(require_role([ROLE_TEACHER]))):
    """Get attendance for a specific date."""
    class_rows = execute_query("SELECT id FROM classes WHERE teacher_id = ?", (user['id'],))
    if not class_rows:
        return {"records": []}

    class_id = class_rows[0]['id']

    rows = execute_query("""
        SELECT s.id, s.name_en, s.name_ur, s.roll_no, COALESCE(a.status, 'present') as status
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        WHERE s.class_id = ?
        ORDER BY s.roll_no
    """, (attendance_date, class_id))

    return {"date": attendance_date, "students": rows_to_list(rows)}


@app.post("/api/teacher/attendance")
async def save_attendance(data: AttendanceSaveRequest, user: dict = Depends(require_role([ROLE_TEACHER]))):
    """Save attendance for a date."""
    class_rows = execute_query("SELECT id FROM classes WHERE teacher_id = ?", (user['id'],))
    if not class_rows:
        raise HTTPException(status_code=400, detail="No class assigned")

    class_id = class_rows[0]['id']

    for record in data.records:
        # Check if attendance already exists
        existing = execute_query(
            "SELECT id FROM attendance WHERE student_id = ? AND date = ?",
            (record.student_id, data.date)
        )

        if existing:
            # Update existing
            execute_update(
                "UPDATE attendance SET status = ?, marked_by = ? WHERE student_id = ? AND date = ?",
                (record.status, user['id'], record.student_id, data.date)
            )
        else:
            # Insert new
            execute_insert(
                "INSERT INTO attendance (student_id, class_id, date, status, marked_by) VALUES (?, ?, ?, ?, ?)",
                (record.student_id, class_id, data.date, record.status, user['id'])
            )

        # Create notification for absent students
        if record.status == STATUS_ABSENT:
            # Check if notification already exists
            existing_notif = execute_query(
                "SELECT id FROM notifications WHERE student_id = ? AND date = ?",
                (record.student_id, data.date)
            )
            if not existing_notif:
                execute_insert(
                    "INSERT INTO notifications (student_id, class_id, date, status) VALUES (?, ?, ?, ?)",
                    (record.student_id, class_id, data.date, NOTIFICATION_PENDING)
                )

    return {"message": "Attendance saved"}


@app.get("/api/teacher/history")
async def get_teacher_history(days: int = 30, user: dict = Depends(require_role([ROLE_TEACHER]))):
    """Get attendance history for teacher's class."""
    class_rows = execute_query("SELECT id FROM classes WHERE teacher_id = ?", (user['id'],))
    if not class_rows:
        return {"students": []}

    class_id = class_rows[0]['id']

    start_date = (date.today() - timedelta(days=days)).isoformat()
    end_date = date.today().isoformat()

    # Get attendance for the date range
    rows = execute_query("""
        SELECT s.id, s.name_en, s.name_ur, s.roll_no,
               a.date, a.status
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date BETWEEN ? AND ?
        WHERE s.class_id = ?
        ORDER BY s.roll_no, a.date
    """, (start_date, end_date, class_id))

    return {"date_range": f"{start_date} to {end_date}", "records": rows_to_list(rows)}


# ==================== PRINCIPAL ROUTES ====================

@app.get("/principal", response_class=HTMLResponse)
async def principal_page(user: dict = Depends(require_role([ROLE_PRINCIPAL]))):
    """Serve principal page."""
    with open("static/principal.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/principal/dashboard")
async def get_dashboard(user: dict = Depends(require_role([ROLE_PRINCIPAL]))):
    """Get daily dashboard with attendance summary."""
    today = date.today().isoformat()

    # Get total students
    total_students = execute_query("SELECT COUNT(*) as count FROM students")[0]['count']

    # Get today's attendance stats
    stats_rows = execute_query("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent,
            SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late
        FROM attendance
        WHERE date = ?
    """, (today,))

    stats = stats_rows[0]
    present = stats['present'] or 0
    absent = stats['absent'] or 0
    late = stats['late'] or 0

    percentage = (present / total_students * 100) if total_students > 0 else 0

    # Get class-wise summary
    class_rows = execute_query("""
        SELECT c.id, c.name, u.name_en as teacher_name,
               (SELECT COUNT(*) FROM students WHERE class_id = c.id) as total_students,
               (SELECT COUNT(*) FROM attendance WHERE class_id = c.id AND date = ? AND status = 'present') as present,
               (SELECT COUNT(*) FROM attendance WHERE class_id = c.id AND date = ? AND status = 'absent') as absent,
               (SELECT COUNT(*) FROM attendance WHERE class_id = c.id AND date = ? AND status = 'late') as late
        FROM classes c
        LEFT JOIN users u ON c.teacher_id = u.id
        ORDER BY c.name
    """, (today, today, today))

    classes = []
    for row in class_rows:
        total = row['total_students']
        present_c = row['present'] or 0
        submitted = total > 0 and (present_c + row['absent'] + row['late']) > 0
        classes.append({
            "class_id": row['id'],
            "class_name": row['name'],
            "teacher_name": row['teacher_name'],
            "total_students": total,
            "present_count": present_c,
            "absent_count": row['absent'] or 0,
            "late_count": row['late'] or 0,
            "attendance_submitted": submitted
        })

    return DashboardResponse(
        date=today,
        stats=DashboardStats(
            total_students=total_students,
            present_count=present,
            absent_count=absent,
            late_count=late,
            percentage=round(percentage, 1)
        ),
        classes=classes
    )


@app.get("/api/principal/report")
async def get_monthly_report(
    year: int,
    month: int,
    class_id: Optional[int] = None,
    user: dict = Depends(require_role([ROLE_PRINCIPAL]))
):
    """Get monthly attendance report data."""
    import calendar

    days_in_month = calendar.monthrange(year, month)[1]
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{days_in_month:02d}"

    # Get students (filtered by class if specified)
    if class_id:
        student_rows = execute_query(
            "SELECT id, name_en, name_ur, roll_no FROM students WHERE class_id = ? ORDER BY roll_no",
            (class_id,)
        )
    else:
        student_rows = execute_query(
            "SELECT id, name_en, name_ur, roll_no FROM students ORDER BY class_id, roll_no"
        )

    # Get attendance for the month
    attendance_rows = execute_query("""
        SELECT student_id, date, status
        FROM attendance
        WHERE date BETWEEN ? AND ?
    """, (start_date, end_date))

    # Build attendance map
    attendance_map: dict[int, dict[str, str]] = {}
    for row in attendance_rows:
        sid = row['student_id']
        if sid not in attendance_map:
            attendance_map[sid] = {}
        day = int(row['date'].split('-')[2])
        attendance_map[sid][str(day)] = row['status']

    students = []
    for student in student_rows:
        sid = student['id']
        student_attendance = attendance_map.get(sid, {})

        # Count present/absent
        present_count = sum(1 for s in student_attendance.values() if s == STATUS_PRESENT)
        absent_count = sum(1 for s in student_attendance.values() if s == STATUS_ABSENT)

        days_counted = present_count + absent_count
        percentage = (present_count / days_counted * 100) if days_counted > 0 else 0

        # Build days dict (1-31)
        days = {}
        for d in range(1, days_in_month + 1):
            days[str(d)] = student_attendance.get(str(d), '-')

        students.append(MonthlyReportStudent(
            student_id=sid,
            name_en=student['name_en'],
            name_ur=student.get('name_ur'),
            roll_no=student['roll_no'],
            days=days,
            total_present=present_count,
            total_absent=absent_count,
            percentage=round(percentage, 1)
        ))

    return MonthlyReportResponse(
        year=year,
        month=month,
        class_id=class_id,
        students=students
    )


@app.get("/api/principal/report/export")
async def export_excel(
    year: int,
    month: int,
    class_id: Optional[int] = None,
    user: dict = Depends(require_role([ROLE_PRINCIPAL]))
):
    """Export monthly report as Excel."""
    from openpyxl import Workbook

    import calendar
    days_in_month = calendar.monthrange(year, month)[1]

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance Report"

    # Header row
    headers = ["Roll No", "Student Name"]
    for d in range(1, days_in_month + 1):
        headers.append(str(d))
    headers.extend(["Total P", "Total A", "%"])
    ws.append(headers)

    # Get students
    if class_id:
        student_rows = execute_query(
            "SELECT id, name_en, roll_no FROM students WHERE class_id = ? ORDER BY roll_no",
            (class_id,)
        )
    else:
        student_rows = execute_query(
            "SELECT id, name_en, roll_no FROM students ORDER BY class_id, roll_no"
        )

    # Get attendance
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{days_in_month:02d}"
    attendance_rows = execute_query("""
        SELECT student_id, date, status
        FROM attendance
        WHERE date BETWEEN ? AND ?
    """, (start_date, end_date))

    attendance_map: dict[int, dict[str, str]] = {}
    for row in attendance_rows:
        sid = row['student_id']
        if sid not in attendance_map:
            attendance_map[sid] = {}
        day = int(row['date'].split('-')[2])
        attendance_map[sid][str(day)] = row['status']

    # Data rows
    for student in student_rows:
        sid = student['id']
        student_attendance = attendance_map.get(sid, {})

        row_data = [student['roll_no'], student['name_en']]
        for d in range(1, days_in_month + 1):
            status = student_attendance.get(str(d), '-')
            # Shorten status
            if status == 'present':
                row_data.append('P')
            elif status == 'absent':
                row_data.append('A')
            elif status == 'late':
                row_data.append('L')
            else:
                row_data.append('-')

        present_count = sum(1 for s in student_attendance.values() if s == STATUS_PRESENT)
        absent_count = sum(1 for s in student_attendance.values() if s == STATUS_ABSENT)
        days_counted = present_count + absent_count
        percentage = (present_count / days_counted * 100) if days_counted > 0 else 0

        row_data.extend([present_count, absent_count, f"{percentage:.1f}%"])
        ws.append(row_data)

    # Save to response
    import io
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    from fastapi.responses import StreamingResponse
    filename = f"attendance_{year}_{month:02d}.xlsx"
    return StreamingResponse(
        buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/api/principal/student/{student_id}")
async def get_student_report(student_id: int, user: dict = Depends(require_role([ROLE_PRINCIPAL]))):
    """Get individual student attendance report."""
    # Get student info
    student_rows = execute_query("SELECT * FROM students WHERE id = ?", (student_id,))
    if not student_rows:
        raise HTTPException(status_code=404, detail="Student not found")

    student = row_to_dict(student_rows[0])

    # Get attendance records
    attendance_rows = execute_query("""
        SELECT date, status
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
    """, (student_id,))

    present = sum(1 for r in attendance_rows if r['status'] == STATUS_PRESENT)
    absent = sum(1 for r in attendance_rows if r['status'] == STATUS_ABSENT)
    late = sum(1 for r in attendance_rows if r['status'] == STATUS_LATE)
    total = len(attendance_rows)
    percentage = (present / total * 100) if total > 0 else 0

    return {
        "student": student,
        "records": rows_to_list(attendance_rows),
        "summary": {
            "total": total,
            "present": present,
            "absent": absent,
            "late": late,
            "percentage": round(percentage, 1)
        }
    }


# ==================== NOTIFICATION ROUTES ====================

@app.get("/api/notifications")
async def get_notifications(status: Optional[str] = None, user: dict = Depends(require_role([ROLE_PRINCIPAL, ROLE_TEACHER]))):
    """Get notifications."""
    if status:
        rows = execute_query("""
            SELECT n.*, s.name_en as student_name, c.name as class_name
            FROM notifications n
            JOIN students s ON n.student_id = s.id
            JOIN classes c ON n.class_id = c.id
            WHERE n.status = ?
            ORDER BY n.created_at DESC
        """, (status,))
    else:
        rows = execute_query("""
            SELECT n.*, s.name_en as student_name, c.name as class_name
            FROM notifications n
            JOIN students s ON n.student_id = s.id
            JOIN classes c ON n.class_id = c.id
            ORDER BY n.created_at DESC
        """)

    return rows_to_list(rows)


@app.post("/api/notifications/{notification_id}/send")
async def mark_notification_sent(notification_id: int, user: dict = Depends(require_role([ROLE_PRINCIPAL]))):
    """Mark notification as sent."""
    execute_update(
        "UPDATE notifications SET status = ? WHERE id = ?",
        (NOTIFICATION_SENT, notification_id)
    )
    return {"message": "Notification marked as sent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
