@echo off
echo ========================================
echo ScreenSage Architect - Quick Start
echo ========================================

echo.
echo [1/3] Setting up Backend (Minimal)...
cd backend

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing minimal dependencies...
pip install -r requirements_minimal.txt

echo.
echo [2/3] Setting up Frontend...
cd ..\frontend

echo Installing frontend dependencies...
call npm install

echo.
echo [3/3] Creating environment files...
cd ..\backend
if not exist .env (
    echo PORT=8000 > .env
    echo DEBUG=true >> .env
    echo OPENAI_API_KEY=dummy_key >> .env
    echo CORS_ORIGINS=["http://localhost:3000"] >> .env
    echo Backend .env created
)

cd ..\frontend
if not exist .env.local (
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
    echo NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws >> .env.local
    echo Frontend .env.local created
)

echo.
echo ========================================
echo Setup Complete! 
echo ========================================
echo.
echo Next steps:
echo 1. Open TWO terminals
echo 2. In terminal 1: start_backend.bat
echo 3. In terminal 2: start_frontend.bat
echo 4. Open: http://localhost:3000
echo.
echo Note: Using minimal setup for quick testing
echo For full AI features, install full requirements later
echo ========================================

pause