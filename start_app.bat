@echo off
echo ==========================================
echo   AI Interview Coach - Automatic Startup
echo ==========================================

:: Start the Backend
echo [1/2] Starting Backend (FastAPI)...
start "Backend Server" cmd /c "cd /d %~dp0backend && .\new_venv\Scripts\python.exe main.py"

:: Give the backend a moment to start
timeout /t 3 /nobreak > nul

:: Start the Frontend
echo [2/2] Starting Frontend (React)...
start "Frontend Server" cmd /c "cd /d %~dp0frontend && npm run dev"

echo.
echo ==========================================
echo   Both servers are starting!
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:8000
echo ==========================================
pause
