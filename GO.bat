@echo off
REM GuardianAI - One Command Startup

echo.
echo ========================================
echo   GuardianAI - Opening in Browser
echo ========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask -q
)

echo Installing/updating dependencies...
pip install -r requirements.txt -q >nul 2>&1

echo.
echo 🚀 Starting GuardianAI...
echo 📱 Opening in browser: http://127.0.0.1:5000
echo 🛑 Press Ctrl+C to stop
echo.

timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

python app_ui.py

pause
