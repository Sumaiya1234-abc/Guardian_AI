# Start GuardianAI Full Stack - Backend + Frontend
Write-Host "🚀 Starting GuardianAI Full Stack..." -ForegroundColor Green

# Install node modules if not present
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "`n📦 Installing frontend dependencies..." -ForegroundColor Yellow
    cd frontend
    npm install
    cd ..
}

# Start backend in background
Write-Host "`n🔧 Starting Backend API on http://localhost:5000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit -Command python backend_api.py"

# Wait 3 seconds for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "🎨 Starting Frontend Dashboard on http://localhost:3000..." -ForegroundColor Cyan
cd frontend
npm start
