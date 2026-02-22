# Pydantic models for School Attendance System
from pydantic import BaseModel
from typing import Optional
from datetime import date


# Auth models
class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    name_en: str
    name_ur: Optional[str] = None
    role: str


# Admin models
class TeacherCreate(BaseModel):
    username: str
    password: str
    name_en: str
    name_ur: Optional[str] = None
    class_id: Optional[int] = None


class TeacherResponse(BaseModel):
    id: int
    username: str
    name_en: str
    name_ur: Optional[str] = None
    class_id: Optional[int] = None
    class_name: Optional[str] = None


class StudentCreate(BaseModel):
    name_en: str
    name_ur: Optional[str] = None
    roll_no: str
    class_id: int
    parent_phone: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    name_en: str
    name_ur: Optional[str] = None
    roll_no: str
    class_id: int
    parent_phone: Optional[str] = None


class ClassCreate(BaseModel):
    name: str
    name_ur: Optional[str] = None


class ClassResponse(BaseModel):
    id: int
    name: str
    name_ur: Optional[str] = None
    teacher_id: Optional[int] = None


class AssignTeacherRequest(BaseModel):
    teacher_id: Optional[int] = None


# Teacher models
class AttendanceRecord(BaseModel):
    student_id: int
    status: str  # present, absent, late


class AttendanceSaveRequest(BaseModel):
    date: str  # YYYY-MM-DD
    records: list[AttendanceRecord]


class StudentWithAttendance(BaseModel):
    id: int
    name_en: str
    name_ur: Optional[str] = None
    roll_no: str
    status: Optional[str] = None


# Principal models
class DashboardStats(BaseModel):
    total_students: int
    present_count: int
    absent_count: int
    late_count: int
    percentage: float


class ClassSummary(BaseModel):
    class_id: int
    class_name: str
    teacher_name: Optional[str] = None
    total_students: int
    present_count: int
    absent_count: int
    late_count: int
    attendance_submitted: bool


class DashboardResponse(BaseModel):
    date: str
    stats: DashboardStats
    classes: list[ClassSummary]


class MonthlyReportStudent(BaseModel):
    student_id: int
    name_en: str
    roll_no: str
    days: dict[str, str]  # day -> status
    total_present: int
    total_absent: int
    percentage: float


class MonthlyReportResponse(BaseModel):
    year: int
    month: int
    class_id: Optional[int] = None
    students: list[MonthlyReportStudent]


# Notification models
class NotificationResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    class_id: int
    class_name: str
    date: str
    status: str
    message: Optional[str] = None


# Error model
class ErrorResponse(BaseModel):
    detail: str
