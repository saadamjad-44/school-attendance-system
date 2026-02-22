# Database module for School Attendance System
# Handles SQLite connection and CRUD operations

import sqlite3
from typing import Any
from constants import DB_FILE


def get_db_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'principal', 'teacher')),
            name_en TEXT NOT NULL,
            name_ur TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Classes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_ur TEXT,
            teacher_id INTEGER REFERENCES users(id)
        )
    """)

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_ur TEXT,
            roll_no TEXT NOT NULL,
            class_id INTEGER NOT NULL REFERENCES classes(id),
            parent_phone TEXT,
            UNIQUE(class_id, roll_no)
        )
    """)

    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id),
            class_id INTEGER NOT NULL REFERENCES classes(id),
            date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late')),
            marked_by INTEGER REFERENCES users(id),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, date)
        )
    """)

    # Notifications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id),
            class_id INTEGER NOT NULL REFERENCES classes(id),
            date TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'sent')),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status)")

    conn.commit()
    conn.close()


def execute_query(query: str, params: tuple = ()) -> list[sqlite3.Row]:
    """Execute a SELECT query and return results."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


def execute_insert(query: str, params: tuple = ()) -> int:
    """Execute an INSERT query and return the last row ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def execute_update(query: str, params: tuple = ()) -> None:
    """Execute an UPDATE or DELETE query."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    """Convert a sqlite3.Row to a dictionary."""
    if row is None:
        return {}
    return dict(row)


def rows_to_list(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    """Convert a list of sqlite3.Row to a list of dictionaries."""
    return [row_to_dict(row) for row in rows]
