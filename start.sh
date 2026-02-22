#!/bin/bash
# School Attendance System - Start Script

echo "Starting School Attendance Management System..."
echo ""

# Check if database exists
if [ ! -f school.db ]; then
    echo "Database not found. Running seed script..."
    python seed_data.py
    echo ""
fi

echo "Starting server on http://localhost:8001"
echo ""
echo "Demo Credentials:"
echo "  Admin:     username='admin',     password='school123'"
echo "  Principal: username='principal', password='school123'"
echo "  Teachers:  username='teacher1-5', password='school123'"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8001)"
