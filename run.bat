@echo off
echo =====================================================================
echo Starting PaperPilot-AI (Backend + Frontend)...
echo =====================================================================

:: Start the FastAPI backend
echo Launching FastAPI Backend...
start "PaperPilot-AI Backend" cmd /k "cd /d %~dp0backend && ..\venv\Scripts\python -m uvicorn main:app --reload --port 8000"

:: Start the Vite frontend
echo Launching React/Vite Frontend...
start "PaperPilot-AI Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both services have been launched in separate windows!
echo - Backend: http://localhost:8000 (Docs: http://localhost:8000/docs)
echo - Frontend: http://localhost:5173
echo =====================================================================
pause
