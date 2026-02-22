# Authentication module for School Attendance System
# Handles password hashing and session management

import bcrypt
from datetime import datetime
from typing import Optional
from database import execute_query, execute_insert, row_to_dict


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_user(username: str, password: str, role: str, name_en: str, name_ur: Optional[str] = None) -> int:
    """Create a new user with hashed password."""
    hashed = hash_password(password)
    return execute_insert(
        "INSERT INTO users (username, password, role, name_en, name_ur) VALUES (?, ?, ?, ?, ?)",
        (username, hashed, role, name_en, name_ur)
    )


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate a user by username and password."""
    rows = execute_query(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    if not rows:
        return None

    user = row_to_dict(rows[0])
    if verify_password(password, user['password']):
        return user
    return None


def get_user_by_id(user_id: int) -> Optional[dict]:
    """Get user by ID."""
    rows = execute_query("SELECT id, username, role, name_en, name_ur, created_at FROM users WHERE id = ?", (user_id,))
    if rows:
        return row_to_dict(rows[0])
    return None


def get_user_by_username(username: str) -> Optional[dict]:
    """Get user by username."""
    rows = execute_query("SELECT * FROM users WHERE username = ?", (username,))
    if rows:
        return row_to_dict(rows[0])
    return None


def get_all_teachers() -> list[dict]:
    """Get all teachers."""
    rows = execute_query("""
        SELECT u.id, u.username, u.name_en, u.name_ur, c.id as class_id, c.name as class_name
        FROM users u
        LEFT JOIN classes c ON u.id = c.teacher_id
        WHERE u.role = 'teacher'
        ORDER BY u.name_en
    """)
    return rows_to_list(rows)


def delete_user(user_id: int) -> None:
    """Delete a user by ID."""
    from database import execute_update
    execute_update("DELETE FROM users WHERE id = ?", (user_id,))


# Session management (in-memory for simplicity)
# In production, use Redis or database-backed sessions
_sessions: dict[str, dict] = {}


def create_session(user_id: int) -> str:
    """Create a new session for a user."""
    session_id = f"{user_id}_{datetime.now().timestamp()}"
    _sessions[session_id] = {
        'user_id': user_id,
        'created_at': datetime.now().isoformat()
    }
    return session_id


def get_session(session_id: str) -> Optional[dict]:
    """Get session data."""
    return _sessions.get(session_id)


def delete_session(session_id: str) -> None:
    """Delete a session."""
    if session_id in _sessions:
        del _sessions[session_id]


def get_user_from_session(session_id: str) -> Optional[dict]:
    """Get user from session ID."""
    session = get_session(session_id)
    if session:
        return get_user_by_id(session['user_id'])
    return None
