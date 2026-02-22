# Tasks: School Attendance Management System

**Input**: Design documents from `/specs/school-attendance/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in root directory
- [X] T002 [P] Create requirements.txt with all dependencies
- [X] T003 [P] Create static/ directory and empty frontend files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Initialize SQLite database schema in database.py (users, classes, students, attendance, notifications tables)
- [X] T005 [P] Implement password hashing utilities in auth.py (bcrypt)
- [X] T006 [P] Create session-based authentication in auth.py (login, logout, get_current_user)
- [X] T007 Create Pydantic models in models.py (User, Class, Student, Attendance, Notification)
- [X] T008 Define application constants in constants.py (roles, status values, messages)
- [X] T009 Setup FastAPI app and middleware in main.py (CORS, sessions, static files)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Admin Login (Priority: P1) 🎯 MVP

**Goal**: Admin can login with username/password, see error on invalid credentials

**Independent Test**: Admin login page works, valid credentials redirect to admin dashboard, invalid shows error

### Implementation for User Story 1

- [X] T010 [P] [US1] Create login HTML page in static/login.html with bilingual labels
- [X] T011 [P] [US1] Create login CSS styles in static/style.css (green/white theme, RTL support)
- [X] T012 [US1] Implement POST /api/login endpoint in main.py (calls auth.py)
- [X] T013 [US1] Implement POST /api/logout endpoint in main.py
- [X] T014 [US1] Implement GET /api/me endpoint in main.py (returns current user)
- [X] T015 [US1] Add session validation middleware in main.py
- [X] T016 [US1] Create admin HTML page in static/admin.html (basic structure)

**Checkpoint**: User Story 1 - Admin Login fully functional

---

## Phase 4: User Story 2 - Teacher Management (Priority: P1)

**Goal**: Admin can add, list, and delete teachers

**Independent Test**: Admin can create teacher with all fields, view teacher list, delete teacher

### Implementation for User Story 2

- [X] T017 [P] [US2] Add teacher section to admin.html
- [X] T018 [P] [US2] Add teacher CRUD functions to static/app.js
- [X] T019 [US2] Implement GET /api/admin/teachers endpoint in main.py
- [X] T020 [US2] Implement POST /api/admin/teachers endpoint in main.py
- [X] T021 [US2] Implement DELETE /api/admin/teachers/{id} endpoint in main.py

**Checkpoint**: User Story 2 - Teacher Management fully functional

---

## Phase 5: User Story 3 - Student Management (Priority: P1)

**Goal**: Admin can add, list by class, and delete students

**Independent Test**: Admin can create student, view students filtered by class, delete student

### Implementation for User Story 3

- [X] T022 [P] [US3] Add student section to admin.html
- [X] T023 [P] [US3] Add student CRUD functions to static/app.js
- [X] T024 [US3] Implement GET /api/admin/students endpoint in main.py (with class_id filter)
- [X] T025 [US3] Implement POST /api/admin/students endpoint in main.py
- [X] T026 [US3] Implement DELETE /api/admin/students/{id} endpoint in main.py

**Checkpoint**: User Story 3 - Student Management fully functional

---

## Phase 6: User Story 4 - Class Management (Priority: P1)

**Goal**: Admin can create classes and assign teachers to classes

**Independent Test**: Admin can create class, view all classes with teachers, assign teacher to class

### Implementation for User Story 4

- [X] T027 [P] [US4] Add class section to admin.html
- [X] T028 [P] [US4] Add class functions to static/app.js
- [X] T029 [US4] Implement GET /api/admin/classes endpoint in main.py
- [X] T030 [US4] Implement POST /api/admin/classes endpoint in main.py
- [X] T031 [US4] Implement PUT /api/admin/classes/{id}/assign-teacher endpoint in main.py

**Checkpoint**: User Story 4 - Class Management fully functional

---

## Phase 7: User Story 5 - Teacher Attendance Marking (Priority: P1)

**Goal**: Teacher can login, view assigned class, mark attendance with Present/Absent/Late

**Independent Test**: Teacher can login, see students with default Present, mark attendance, save for today, edit existing

### Implementation for User Story 5

- [X] T032 [P] [US5] Create teacher HTML page in static/teacher.html
- [X] T033 [P] [US5] Add teacher functions to static/app.js (fetch students, save attendance)
- [X] T034 [US5] Implement GET /api/teacher/my-class endpoint in main.py (returns class + students)
- [X] T035 [US5] Implement GET /api/teacher/attendance/{date} endpoint in main.py
- [X] T036 [US5] Implement POST /api/teacher/attendance endpoint in main.py (save/update, create notifications for absent)
- [X] T037 [US5] Implement role-based routing redirect in main.py (teacher -> /teacher page)

**Checkpoint**: User Story 5 - Teacher Attendance Marking fully functional

---

## Phase 8: User Story 6 - Notification System (Priority: P2)

**Goal**: Absent students create notification records, Principal can view and mark as sent

**Independent Test**: Absent mark creates notification, Principal sees pending list, can mark sent

### Implementation for User Story 6

- [X] T038 [P] [US6] Add notification handling in attendance save (T036 already creates notifications)
- [X] T039 [US6] Implement GET /api/notifications endpoint in main.py
- [X] T040 [US6] Implement POST /api/notifications/{id}/send endpoint in main.py

**Checkpoint**: User Story 6 - Notification System fully functional

---

## Phase 9: User Story 7 - Principal Daily Dashboard (Priority: P1)

**Goal**: Principal sees daily attendance summary with totals and percentages, class-wise table

**Independent Test**: Principal login shows dashboard with today's stats, class table, highlights missing attendance

### Implementation for User Story 7

- [X] T041 [P] [US7] Create principal HTML page in static/principal.html
- [X] T042 [P] [US7] Add principal dashboard functions to static/app.js
- [X] T043 [US7] Implement GET /api/principal/dashboard endpoint in main.py (totals, percentages, class summary)
- [X] T044 [US7] Add missing attendance highlighting logic in main.py

**Checkpoint**: User Story 7 - Principal Dashboard fully functional

---

## Phase 10: User Story 8 - Monthly Report & Excel Download (Priority: P2)

**Goal**: Principal can view monthly report and download Excel with daily attendance

**Independent Test**: Principal can select month, see class summary, download .xlsx file

### Implementation for User Story 8

- [X] T045 [P] [US8] Add report section to principal.html (month selector, download button)
- [X] T046 [P] [US8] Add report functions to static/app.js
- [X] T047 [US8] Implement GET /api/principal/report endpoint in main.py (monthly data)
- [X] T048 [US8] Implement Excel export in reports.py (openpyxl, columns: Roll No, Name, 1-31, Total P, Total A, %)
- [X] T049 [US8] Implement GET /api/principal/report/export endpoint in main.py (serves Excel file)

**Checkpoint**: User Story 8 - Monthly Report & Excel Download fully functional

---

## Phase 11: User Story 9 - Student Wise Report (Priority: P2)

**Goal**: Principal can view individual student attendance history with totals

**Independent Test**: Principal selects student, sees all records with present/absent/late counts

### Implementation for User Story 9

- [X] T050 [P] [US9] Add student search/select to principal.html
- [X] T051 [US9] Implement GET /api/principal/student/{id} endpoint in main.py

**Checkpoint**: User Story 9 - Student Wise Report fully functional

---

## Phase 12: User Story 10 - Teacher Class History (Priority: P2)

**Goal**: Teacher can view past 30 days attendance for their class

**Independent Test**: Teacher sees history page with past 30 days, absence counts per student

### Implementation for User Story 10

- [X] T052 [P] [US10] Add history section to teacher.html
- [X] T053 [US10] Implement GET /api/teacher/history endpoint in main.py (past 30 days, student absence counts)

**Checkpoint**: User Story 10 - Teacher Class History fully functional

---

## Phase 13: User Story 11 - Sample Data Seeding (Priority: P1)

**Goal**: App starts with sample data: 1 admin, 1 principal, 5 teachers, 8 classes, 160 students

**Independent Test**: App runs, seed data exists, all demo logins work with password 'school123'

### Implementation for User Story 11

- [X] T054 [US11] Create seed_data.py to insert sample data on first run
- [X] T055 [US11] Integrate seed_data into main.py startup (check if data exists, insert if not)
- [X] T056 [US11] Create README.md with demo credentials and quick start

**Checkpoint**: User Story 11 - Sample Data Seeding fully functional

---

## Phase 14: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T057 [P] Add responsive CSS for mobile in static/style.css
- [X] T058 [P] Verify all Urdu/English bilingual labels in HTML files
- [X] T059 Add error handling UI feedback in static/app.js
- [X] T060 Final integration test - verify all user stories work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-13)**: All depend on Foundational phase completion
  - User stories proceed sequentially in priority order (P1 → P2)
- **Polish (Phase 14)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 Admin Login (P1)**: Can start after Foundational - No dependencies on other stories
- **US2 Teacher Management (P1)**: Depends on US1 (admin dashboard exists)
- **US3 Student Management (P1)**: Depends on US1
- **US4 Class Management (P1)**: Depends on US2 (needs teachers to assign)
- **US5 Teacher Attendance (P1)**: Depends on US2, US3, US4 (needs teachers, students, classes)
- **US6 Notifications (P2)**: Depends on US5 (attendance creates notifications)
- **US7 Principal Dashboard (P1)**: Depends on US5 (needs attendance data)
- **US8 Monthly Report (P2)**: Depends on US7
- **US9 Student Report (P2)**: Depends on US7
- **US10 Teacher History (P2)**: Depends on US5
- **US11 Seed Data (P1)**: Can be done anytime after Foundational (best done early for testing)

### Within Each User Story

- Core implementation before UI integration
- Story complete before moving to next priority

### Parallel Opportunities

- T002, T003 can run in parallel (Setup)
- T005, T006, T007, T008 can run in parallel (Foundational)
- T010, T011 can run in parallel (US1)
- T017, T018 can run in parallel (US2)
- T022, T023 can run in parallel (US3)
- T027, T028 can run in parallel (US4)
- T032, T033 can run in parallel (US5)
- T041, T042 can run in parallel (US7)
- T045, T046 can run in parallel (US8)
- T050 can run in parallel with T045-T046

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Admin Login)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → Test independently → Deploy/Demo (MVP!)
3. Add US2-US4 → Test → Deploy/Demo
4. Add US5-US7 → Test → Deploy/Demo
5. Add US8-US11 → Test → Deploy/Demo
6. Each story adds value without breaking previous stories

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 60 |
| Setup Phase | 3 |
| Foundational Phase | 6 |
| User Story Phases | 48 |
| Polish Phase | 4 |
| Parallelizable Tasks | 20 |

### Task Count Per User Story

| User Story | Tasks | Priority |
|------------|-------|----------|
| US1 - Admin Login | 7 | P1 |
| US2 - Teacher Management | 5 | P1 |
| US3 - Student Management | 5 | P1 |
| US4 - Class Management | 5 | P1 |
| US5 - Teacher Attendance | 6 | P1 |
| US6 - Notifications | 3 | P2 |
| US7 - Principal Dashboard | 4 | P1 |
| US8 - Monthly Report | 5 | P2 |
| US9 - Student Report | 2 | P2 |
| US10 - Teacher History | 2 | P2 |
| US11 - Seed Data | 3 | P1 |

### Suggested MVP Scope

- **MVP (Phase 3 + Phase 7)**: Admin Login + Teacher Attendance = Core attendance marking
- **Phase 1**: Setup + Foundational + US1 + US2 + US3 + US4 + US5 + US11
- **Full**: All 11 user stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
