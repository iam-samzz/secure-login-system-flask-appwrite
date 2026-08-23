@echo off
REM Windows launcher: starts a Python HTTP server and opens index.html
REM Double-click this .bat file to run.
cd /d "%~dp0"
where python >nul 2>&1
if %errorlevel% neq 0 (
  echo Python not found. Please install Python 3.
  pause
  exit /b 1
)
set PORT=8000
set URL=http://localhost:%PORT%/index.html
start "" "%URL%"
REM Start server in this window so the user can see logs. Use Ctrl+C to stop.
python -m http.server %PORT%
pause