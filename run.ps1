Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Starting PaperPilot-AI (Backend + Frontend)..." -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

# Start Backend
Write-Host "Launching FastAPI Backend..." -ForegroundColor Green
Start-Process cmd -ArgumentList "/k cd /d `"$PSScriptRoot\backend`" && ..\venv\Scripts\python -m uvicorn main:app --reload --port 8000" -WindowStyle Normal

# Start Frontend
Write-Host "Launching React/Vite Frontend..." -ForegroundColor Green
Start-Process cmd -ArgumentList "/k cd /d `"$PSScriptRoot\frontend`" && npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "Both services have been launched in separate windows!" -ForegroundColor Yellow
Write-Host "- Backend: http://localhost:8000 (Docs: http://localhost:8000/docs)" -ForegroundColor Yellow
Write-Host "- Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan
