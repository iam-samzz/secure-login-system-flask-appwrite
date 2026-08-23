@echo off
echo Starting Secure Login System...



pip install -r requirements.txt >nul 2>&1

if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your database.
    pause
    exit /b 1
)

echo Server starting at http://localhost:5000
python app.py