// School Attendance - Shared JavaScript

const API_BASE = '/api';

// Utility functions
function showError(message) {
    const errorEl = document.getElementById('error');
    if (errorEl) errorEl.textContent = message;
}

function showSuccess(message) {
    const successEl = document.getElementById('success');
    if (successEl) successEl.textContent = message;
}

function clearMessages() {
    const errorEl = document.getElementById('error');
    const successEl = document.getElementById('success');
    if (errorEl) errorEl.textContent = '';
    if (successEl) successEl.textContent = '';
}

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        credentials: 'include',
        ...options,
    };

    if (options.body && typeof options.body === 'object') {
        config.headers = {
            'Content-Type': 'application/json',
            ...config.headers,
        };
        config.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, config);

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new Error(error.detail || 'Request failed');
    }

    return response.json();
}

// Auth functions
async function login(username, password) {
    const data = await apiRequest('/login', {
        method: 'POST',
        body: { username, password },
    });
    return data;
}

async function logout() {
    await apiRequest('/logout', { method: 'POST' });
}

async function getCurrentUser() {
    try {
        return await apiRequest('/me');
    } catch {
        return null;
    }
}

// Admin functions - Teachers
async function getTeachers() {
    return apiRequest('/admin/teachers');
}

async function addTeacher(teacherData) {
    return apiRequest('/admin/teachers', {
        method: 'POST',
        body: teacherData,
    });
}

async function deleteTeacher(id) {
    return apiRequest(`/admin/teachers/${id}`, {
        method: 'DELETE',
    });
}

// Admin functions - Students
async function getStudents(classId = null) {
    const params = classId ? `?class_id=${classId}` : '';
    return apiRequest(`/admin/students${params}`);
}

async function addStudent(studentData) {
    return apiRequest('/admin/students', {
        method: 'POST',
        body: studentData,
    });
}

async function deleteStudent(id) {
    return apiRequest(`/admin/students/${id}`, {
        method: 'DELETE',
    });
}

// Admin functions - Classes
async function getClasses() {
    return apiRequest('/admin/classes');
}

async function addClass(classData) {
    return apiRequest('/admin/classes', {
        method: 'POST',
        body: classData,
    });
}

async function assignTeacher(classId, teacherId) {
    return apiRequest(`/admin/classes/${classId}/assign-teacher`, {
        method: 'PUT',
        body: { teacher_id: teacherId },
    });
}

// Teacher functions
async function getMyClass() {
    return apiRequest('/teacher/my-class');
}

async function getAttendance(date) {
    return apiRequest(`/teacher/attendance/${date}`);
}

async function saveAttendance(date, records) {
    return apiRequest('/teacher/attendance', {
        method: 'POST',
        body: { date, records },
    });
}

async function getAttendanceHistory(days = 30) {
    return apiRequest(`/teacher/history?days=${days}`);
}

// Principal functions
async function getDashboard() {
    return apiRequest('/principal/dashboard');
}

async function getMonthlyReport(year, month, classId = null) {
    const params = `?year=${year}&month=${month}${classId ? `&class_id=${classId}` : ''}`;
    return apiRequest(`/principal/report${params}`);
}

async function downloadExcel(year, month, classId = null) {
    const params = `?year=${year}&month=${month}${classId ? `&class_id=${classId}` : ''}`;
    window.location.href = `${API_BASE}/principal/report/export${params}`;
}

async function getStudentReport(studentId) {
    return apiRequest(`/principal/student/${studentId}`);
}

// Notification functions
async function getNotifications(status = null) {
    const params = status ? `?status=${status}` : '';
    return apiRequest(`/notifications${params}`);
}

async function markNotificationSent(id) {
    return apiRequest(`/notifications/${id}/send`, {
        method: 'POST',
    });
}

// UI helpers
function redirectToRole(user) {
    if (!user) {
        window.location.href = '/login';
        return;
    }

    const rolePages = {
        admin: '/admin',
        principal: '/principal',
        teacher: '/teacher',
    };

    const targetPage = rolePages[user.role];
    if (targetPage && window.location.pathname !== targetPage) {
        window.location.href = targetPage;
    }
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ur-PK');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Check auth for protected pages
    const protectedPages = ['/admin', '/principal', '/teacher'];
    const currentPath = window.location.pathname;

    if (protectedPages.includes(currentPath)) {
        const user = await getCurrentUser();
        if (!user) {
            window.location.href = '/login';
            return;
        }
    }
});
