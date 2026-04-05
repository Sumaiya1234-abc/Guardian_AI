@echo off
REM Start GuardianAI Modern UI

echo.
echo ========================================
echo   GuardianAI - Modern Web Interface
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
)

echo.
echo Starting GuardianAI on http://127.0.0.1:5000...
echo Press Ctrl+C to stop.
echo.

python app_ui.py

pause
