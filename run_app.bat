@echo off
title Festive Demand Forecast AI - Full App Launcher
echo =========================================================
echo   Starting Festive Demand Forecast AI (Backend + Frontend)
echo =========================================================

echo.
echo [1/2] Starting Flask Backend Server (Port 5000)...
start "Festive AI - Backend Server" cmd /k "cd /d ""%~dp0backend"" && ""..\.venv\Scripts\python.exe"" app.py"

echo [2/2] Starting Vite React Frontend (Port 5173)...
start "Festive AI - Frontend Server" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"

echo.
echo Waiting 3 seconds for servers to initialize...
timeout /t 3 /nobreak >nul

echo.
echo Launching Web Dashboard in your browser...
start http://localhost:5173

echo.
echo =========================================================
echo   Both servers have been launched in separate windows!
echo   * Backend:  http://127.0.0.1:5000
echo   * Frontend: http://localhost:5173
echo =========================================================
echo You can close this launcher window anytime.
pause
