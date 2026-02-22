@echo off
REM School Attendance System - Start Script
REM This script will find an available port and start the server

echo ========================================
echo School Attendance Management System
echo ========================================
echo.

REM Check if database exists
if not exist school.db (
    echo [INFO] Database not found. Running seed script...
    python seed_data.py
    if errorlevel 1 (
        echo [ERROR] Failed to seed database
        pause
        exit /b 1
    )
    echo.
)

echo [INFO] Starting server...
echo.
echo Demo Credentials:
echo   Admin:     username='admin',     password='school123'
echo   Principal: username='principal', password='school123'
echo   Teachers:  username='teacher1-5', password='school123'
echo.

REM Try ports 8000-8010 until we find one available
for /L %%p in (8000,1,8010) do (
    netstat -ano | find ":%%p " | find "LISTENING" >nul
    if errorlevel 1 (
        echo [INFO] Starting server on http://localhost:%%p
        echo [INFO] Press Ctrl+C to stop the server
        echo.
        python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=%%p)"
        goto :end
    )
)

echo [ERROR] No available ports found between 8000-8010
pause

:end
