# Application Constants for School Attendance System

# User roles
ROLE_ADMIN = "admin"
ROLE_PRINCIPAL = "principal"
ROLE_TEACHER = "teacher"

ROLES = [ROLE_ADMIN, ROLE_PRINCIPAL, ROLE_TEACHER]

# Attendance status
STATUS_PRESENT = "present"
STATUS_ABSENT = "absent"
STATUS_LATE = "late"

ATTENDANCE_STATUSES = [STATUS_PRESENT, STATUS_ABSENT, STATUS_LATE]

# Notification status
NOTIFICATION_PENDING = "pending"
NOTIFICATION_SENT = "sent"

# Database
DB_FILE = "school.db"

# Session
SESSION_COOKIE_NAME = "session"

# Messages
MSG_INVALID_CREDENTIALS = "Invalid username or password"
MSG_LOGIN_SUCCESS = "Login successful"
MSG_LOGOUT_SUCCESS = "Logout successful"
MSG_REQUIRED_FIELD = "This field is required"
MSG_TEACHER_ADDED = "Teacher added successfully"
MSG_TEACHER_DELETED = "Teacher deleted successfully"
MSG_STUDENT_ADDED = "Student added successfully"
MSG_STUDENT_DELETED = "Student deleted successfully"
MSG_CLASS_ADDED = "Class added successfully"
MSG_ATTENDANCE_SAVED = "Attendance saved successfully"

# Urdu translations for UI labels
LABELS = {
    # Common
    "login": "Login / لاگ ان",
    "logout": "Logout / لاگ آوٹ",
    "save": "Save / محفوظ کریں",
    "cancel": "Cancel / رد کریں",
    "delete": "Delete / حذف کریں",
    "edit": "Edit / ترمیم کریں",
    "add": "Add / شامل کریں",
    "search": "Search / تلاش کریں",

    # User roles
    "admin": "Admin / منتظم",
    "principal": "Principal / پرنسپل",
    "teacher": "Teacher / استاد",

    # Attendance
    "present": "Present / حاضر",
    "absent": "Absent / غائب",
    "late": "Late / دیر سے",
    "attendance": "Attendance / حاضری",

    # Dashboard
    "dashboard": "Dashboard / ڈیش بورڈ",
    "total_students": "Total Students / کل طلباء",
    "present_count": "Present / حاضر",
    "absent_count": "Absent / غائب",
    "late_count": "Late / دیر سے",
    "percentage": "Percentage / فیصدہ",

    # Reports
    "reports": "Reports / رپورٹس",
    "monthly_report": "Monthly Report / ماہانہ رپورٹ",
    "download_excel": "Download Excel / ایکسل ڈاؤنلوڈ کریں",

    # Notifications
    "notifications": "Notifications / اطلاعات",
    "send": "Send / بھیجیں",
    "pending": "Pending / زیر التوا",
    "sent": "Sent / بھیجی گئی",

    # Management
    "teachers": "Teachers / استاد",
    "students": "Students / طلباء",
    "classes": "Classes / کلاسز",

    # Fields
    "name": "Name / نام",
    "username": "Username / صارف نام",
    "password": "Password / پاس ورڈ",
    "roll_number": "Roll No / رول نمبر",
    "class": "Class / کلاس",
    "phone": "Phone / فون",
    "date": "Date / تاریخ",
}
