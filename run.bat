@echo off
REM Start GuardianAI Full Stack - Backend + Frontend

echo.
echo ========================================
echo   GuardianAI Full Stack Launcher
echo ========================================
echo.

REM Navigate to project root
cd /d "%~dp0"

REM Check and install node_modules
if not exist "frontend\node_modules" (
    echo.
    echo [1/3] Installing frontend dependencies (this may take 2-3 minutes)...
    echo.
    cd frontend
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed. Make sure Node.js is installed.
        pause
        exit /b 1
    )
    cd ..
    echo Done with npm install
    echo.
)

REM Start backend
echo [2/3] Starting Backend API on http://localhost:5000...
echo.
start cmd /k "python backend_api.py"

REM Wait for backend to start
timeout /t 4

REM Start frontend
echo [3/3] Starting Frontend Dashboard on http://localhost:3000...
echo.
cd frontend
start cmd /k "npm start"

echo.
echo ========================================
echo   Dashboard loading...
echo ========================================
echo.
echo Dashboard URL: http://localhost:3000
echo Backend API:  http://localhost:5000
echo.
echo (This window will close in 5 seconds)
echo ========================================
echo.

timeout /t 5
