# Data Model: School Attendance Management System

## Entities

### 1. User
Represents all system users (admin, principal, teacher).

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user ID |
| username | TEXT | UNIQUE NOT NULL | Login username |
| password_hash | TEXT | NOT NULL | bcrypt hashed password |
| role | TEXT | NOT NULL | admin, principal, or teacher |
| name | TEXT | NOT NULL | Full display name |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation time |

**Validation Rules:**
- username: 3-50 characters, alphanumeric + underscore
- password: minimum 6 characters
- role: must be one of 'admin', 'principal', 'teacher'

### 2. Class
Represents school classes/grades.

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique class ID |
| name | TEXT | UNIQUE NOT NULL | Class name (e.g., "6-A") |
| teacher_id | INTEGER | FOREIGN KEY (User.id), NULLABLE | Assigned class teacher |

**Validation Rules:**
- name: 1-20 characters, alphanumeric with dash allowed

### 3. Student
Represents enrolled students.

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique student ID |
| name | TEXT | NOT NULL | Student full name |
| roll_number | TEXT | NOT NULL | Unique roll number within class |
| class_id | INTEGER | FOREIGN KEY (Class.id) | Enrolled class |
| parent_contact | TEXT | NULLABLE | Parent phone number |

**Validation Rules:**
- name: 2-100 characters
- roll_number: 1-20 characters, unique within class
- parent_contact: optional, phone format

### 4. Attendance
Records daily attendance for each student.

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique record ID |
| student_id | INTEGER | FOREIGN KEY (Student.id), NOT NULL | Student reference |
| date | DATE | NOT NULL | Attendance date |
| status | TEXT | NOT NULL | present, absent, or late |
| marked_by | INTEGER | FOREIGN KEY (User.id) | Teacher who marked |

**Validation Rules:**
- date: cannot be future date
- status: must be 'present', 'absent', or 'late'
- UNIQUE(student_id, date) - one record per student per day

### 5. Notification
Tracks parent notifications for absent students.

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique notification ID |
| student_id | INTEGER | FOREIGN KEY (Student.id) | Absent student |
| class_id | INTEGER | FOREIGN KEY (Class.id) | Student class |
| date | DATE | NOT NULL | Date student was absent |
| status | TEXT | DEFAULT 'pending' | pending or sent |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Validation Rules:**
- status: must be 'pending' or 'sent'

## Relationships

```
User (teacher)
  ↑
  └── Class (teacher_id)

Class
  ↑
  └── Student (class_id)

Student
  ↑
  ├── Attendance (student_id)
  └── Notification (student_id)

User (teacher)
  ↑
  └── Attendance (marked_by)

Class
  ↑
  └── Notification (class_id)
```

## Database Schema (SQL)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'principal', 'teacher')),
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    teacher_id INTEGER REFERENCES users(id)
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT NOT NULL,
    class_id INTEGER NOT NULL REFERENCES classes(id),
    parent_contact TEXT,
    UNIQUE(class_id, roll_number)
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id),
    date DATE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late')),
    marked_by INTEGER REFERENCES users(id),
    UNIQUE(student_id, date)
);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id),
    class_id INTEGER NOT NULL REFERENCES classes(id),
    date DATE NOT NULL,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'sent')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Indexes

```sql
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_attendance_student ON attendance(student_id);
CREATE INDEX idx_students_class ON students(class_id);
CREATE INDEX idx_notifications_status ON notifications(status);
```
