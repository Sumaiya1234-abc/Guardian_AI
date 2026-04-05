# Start GuardianAI Modern Web UI

Write-Host "🛡️ GuardianAI - Modern Web Interface" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Check if Flask is installed
try {
    python -c "import flask" 2>$null
} catch {
    Write-Host "📦 Installing Flask..." -ForegroundColor Yellow
    pip install flask
}

Write-Host ""
Write-Host "🚀 Starting GuardianAI on http://127.0.0.1:5000..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

python app_ui.py
