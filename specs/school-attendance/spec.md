# Feature Specification: School Attendance Management System

**Feature Branch**: `school-attendance`
**Created**: 2026-02-22
**Status**: Draft
**Input**: User description: "Build a School Attendance Management System for Pakistani schools — bilingual (Urdu + English)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Admin Login (Priority: P1)

Admin apni ID aur password se login kare. Galat password pe clear error message aaye.

**Why this priority**: Admin login sabse pehla interaction hai — bina login ke koi bhi management kaam nahi ho sakta.

**Independent Test**: Admin login page khulne ke baad valid credentials se login ho jaye. Invalid credentials pe error dikhe.

**Acceptance Scenarios**:

1. **Given** admin is on login page, **When** enters valid admin ID and password, **Then** redirected to admin dashboard
2. **Given** admin is on login page, **When** enters wrong password, **Then** clear error message "Invalid credentials" dikhe
3. **Given** admin is on login page, **When** leaves fields empty, **Then** validation error dikhe

---

### User Story 2 - Teacher Management (Priority: P1)

Admin nayi teacher add kar sake: naam, ID, password, assigned class. Teachers ki list dekho aur teacher delete kar sake.

**Why this priority**: Teacher management admin ka core kaam hai — bina teacher ke attendance mark nahi ho sakti.

**Independent Test**: Admin dashboard se teacher add, list, aur delete kar sake.

**Acceptance Scenarios**:

1. **Given** admin is on teachers page, **When** adds new teacher with all fields, **Then** teacher saved in database
2. **Given** admin is on teachers page, **When** views teacher list, **Then** all teachers displayed with name, ID, assigned class
3. **Given** admin is on teachers page, **When** deletes a teacher, **Then** teacher removed from database

---

### User Story 3 - Student Management (Priority: P1)

Admin nayi student add kar sake: naam, roll number, class. Class ke hisaab se students dekho aur student delete kar sake.

**Why this priority**: Students core entities hain — unki attendance track hogi.

**Independent Test**: Admin dashboard se student add, view by class, aur delete kar sake.

**Acceptance Scenarios**:

1. **Given** admin is on students page, **When** adds new student with all fields, **Then** student saved in database
2. **Given** admin selects a class, **When** views students, **Then** all students of that class displayed
3. **Given** admin is on students page, **When** deletes a student, **Then** student removed from database

---

### User Story 4 - Class Management (Priority: P1)

Admin classes define kar sake: e.g. Class 1-A, 2-B, 10-A. Har class mein teacher assign kar sake.

**Why this priority**: Classes attendance ke liye organizational unit hain.

**Independent Test**: Admin classes create kar sake aur teacher assign kar sake.

**Acceptance Scenarios**:

1. **Given** admin is on classes page, **When** creates new class, **Then** class saved in database
2. **Given** admin is on classes page, **When** assigns teacher to class, **Then** teacher-class relationship saved
3. **Given** admin views classes, **Then** all classes displayed with assigned teacher

---

### User Story 5 - Teacher Login & Attendance Marking (Priority: P1)

Teacher apni ID aur password se login kare. Login ke baad seedha apni assigned class dekhe. Har student ke liye Present/Absent/Late buttons ho. Default: sab Present selected ho. Date automatic aaj ki ho. "Save Attendance" button save kare. Agar aaj ki attendance pehle se save hai to existing data edit ke liye dikhe.

**Why this priority**: Teacher ka core kaam attendance mark karna hai — ye system ka sabse important feature hai.

**Independent Test**: Teacher login karke attendance mark kar sake aur save kar sake.

**Acceptance Scenarios**:

1. **Given** teacher logs in, **When** views their assigned class, **Then** all students of that class displayed with default "Present" selected
2. **Given** teacher is on attendance page, **When** marks student as Absent, **Then** status saved as "Absent"
3. **Given** teacher is on attendance page, **When** marks student as Late, **Then** status saved as "Late"
4. **Given** teacher clicks Save Attendance, **When** all students marked, **Then** attendance saved for today's date
5. **Given** teacher returns same day, **When** views attendance page, **Then** existing attendance data displayed for editing

---

### User Story 6 - Notification System (Priority: P2)

Jab student absent mark ho, notification table mein record ban jaye: student naam, class, date, parent contact. Principal ke dashboard pe pending notifications dikhen. "Send" button se status "sent" ho jaye.

**Why this priority**: Parents ko inform karna important hai — Phase 2 mein real WhatsApp/SMS aayega.

**Independent Test**: Absent student ke liye notification create ho jaye aur principal send kar sake.

**Acceptance Scenarios**:

1. **Given** teacher marks student as Absent, **When** saves attendance, **Then** notification record created automatically
2. **Given** principal views notifications, **When** pending notifications exist, **Then** list of absent students displayed
3. **Given** principal clicks Send, **When** notification marked as sent, **Then** status updated to "sent"

---

### User Story 7 - Principal Daily Dashboard (Priority: P1)

Principal login kare. Aaj ki overall attendance dekhe: Total students, Present/Absent/Late count, Percentage. Har class ki summary table. Jo class ne abhi attendance nahi di — highlight ho.

**Why this priority**: Principal ko daily overview chahiye — school ki performance track karne ke liye.

**Independent Test**: Principal login karke daily dashboard dekhe.

**Acceptance Scenarios**:

1. **Given** principal logs in, **When** views daily dashboard, **Then** today's total attendance stats displayed
2. **Given** principal views dashboard, **When** classes exist, **Then** class-wise summary table shown
3. **Given** principal views dashboard, **When** a class hasn't submitted attendance, **Then** that class highlighted in red/yellow

---

### User Story 8 - Monthly Report & Excel Download (Priority: P2)

Principal month select kare. Class-wise attendance summary dikhe. "Excel Download" button — .xlsx file download ho. Excel mein: Student naam, Roll No, har din ka status, Total present days, Percentage.

**Why this priority**: Monthly reports parents aur authorities ko certify karne ke liye chahiye.

**Independent Test**: Principal month select karke Excel download kar sake.

**Acceptance Scenarios**:

1. **Given** principal selects month, **When** views report, **Then** class-wise summary displayed
2. **Given** principal clicks Excel Download, **When** month selected, **Then** .xlsx file downloads with all data
3. **Given** Excel file opened, **When** data verified, **Then** contains student name, roll number, daily status, total present, percentage

---

### User Story 9 - Student Wise Report (Priority: P2)

Principal kisi ek student ka poora record dekho. Kitne din present, absent, late.

**Why this priority**: Individual student ki performance track karne ke liye.

**Independent Test**: Principal student select karke uska full attendance history dekhe.

**Acceptance Scenarios**:

1. **Given** principal selects student, **When** views report, **Then** all attendance records displayed
2. **Given** principal views student report, **When** data exists, **Then** shown: total present days, absent days, late days

---

### User Story 10 - Teacher Class History (Priority: P2)

Teacher apni class ki past 30 din ki attendance dekh sake. Kon kitne din absent raha.

**Why this priority**: Teacher ko apni class ki performance dekhni chahiye.

**Independent Test**: Teacher class history page dekhe.

**Acceptance Scenarios**:

1. **Given** teacher views class history, **When** selects date range, **Then** attendance records displayed
2. **Given** teacher views history, **When** student has multiple absences, **Then** absence count shown per student

---

### User Story 11 - Sample Data Seeding (Priority: P1)

App start hote hi yeh data ready ho: 1 Admin account, 1 Principal account, 5 Teachers (har ek ki ek class assigned), 8 Classes: Class 6-A, 6-B, 7-A, 7-B, 8-A, 8B, 9-A, 10-A, Har class mein 20 students. Passwords: 'school123' sab ke liye (demo ke liye).

**Why this priority**: Testing aur demo ke liye ready data chahiye.

**Independent Test**: App run hone ke baad seed data automatically inserted ho.

**Acceptance Scenarios**:

1. **Given** app starts first time, **When** seed_data.py runs, **Then** all sample data created
2. **Given** seed data exists, **When** users login with 'school123', **Then** login successful

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate users (admin, principal, teacher) via session-based login with username and password
- **FR-002**: System MUST validate credentials and return appropriate error messages for invalid login
- **FR-003**: Admin MUST be able to create, view, and delete teachers with fields: name, teacher_id, password, assigned_class_id
- **FR-004**: Admin MUST be able to create, view by class, and delete students with fields: name, roll_number, class_id
- **FR-005**: Admin MUST be able to create classes and assign teachers to classes
- **FR-006**: Teacher MUST be able to view their assigned class students
- **FR-007**: Teacher MUST be able to mark attendance with three states: Present (حاضر), Absent (غائب), Late (دیر سے)
- **FR-008**: Teacher MUST be able to save attendance for current date
- **FR-009**: Teacher MUST be able to edit existing attendance for current date
- **FR-010**: System MUST automatically set current date for attendance
- **FR-011**: Default attendance status MUST be "Present" for all students
- **FR-012**: System MUST create notification record when student is marked Absent
- **FR-013**: Principal MUST be able to view daily attendance dashboard with totals and percentages
- **FR-014**: Principal MUST be able to view class-wise attendance summary
- **FR-015**: System MUST highlight classes that haven't submitted attendance
- **FR-016**: Principal MUST be able to download monthly report as Excel (.xlsx)
- **FR-017**: Excel report MUST contain: student name, roll number, daily status, total present days, percentage
- **FR-018**: Principal MUST be able to view individual student attendance history
- **FR-019**: Teacher MUST be able to view past 30 days attendance for their class
- **FR-020**: System MUST seed sample data on first run (1 admin, 1 principal, 5 teachers, 8 classes, 160 students)
- **FR-021**: System MUST use bcrypt for password hashing
- **FR-022**: System MUST enforce role-based access control (teacher cannot access admin pages, etc.)

### Key Entities *(include if feature involves data)*

- **User**: id, username, password_hash, role (admin/principal/teacher), created_at
- **Class**: id, name, teacher_id (assigned teacher)
- **Student**: id, name, roll_number, class_id, parent_contact
- **Attendance**: id, student_id, date, status (present/absent/late), marked_by_teacher_id
- **Notification**: id, student_id, class_id, date, status (pending/sent), created_at

### Non-Functional Requirements

- **NFR-001**: Mobile responsive design - UI must work on mobile devices
- **NFR-002**: Bilingual UI - All labels in Urdu + English with `lang=ur` and RTL support
- **NFR-003**: Green and white school theme
- **NFR-004**: Fast page load - static HTML/JS, no heavy frameworks
- **NFR-005**: Fully local - no internet required, SQLite database

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Admin can create teacher, student, and class in under 30 seconds each
- **SC-002**: Teacher can mark attendance for 20 students in under 2 minutes
- **SC-003**: Principal can download monthly Excel report in under 5 seconds
- **SC-004**: 100% of user interactions produce appropriate UI feedback (success/error messages)
- **SC-005**: All pages load within 2 seconds on standard hardware
