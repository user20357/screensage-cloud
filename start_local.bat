@echo off
echo ========================================
echo ScreenSage Architect - Local Development
echo ========================================

echo.
echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing backend dependencies...
pip install -r requirements.txt

echo.
echo [2/4] Setting up Frontend...
cd ..\frontend

echo Installing frontend dependencies...
call npm install

echo.
echo [3/4] Creating environment files...
cd ..\backend
if not exist .env (
    copy .env.example .env
    echo Backend .env created - please edit with your API keys
)

cd ..\frontend
if not exist .env.local (
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
    echo NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws >> .env.local
    echo Frontend .env.local created
)

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Edit backend\.env with your OpenAI API key (optional)
echo 2. Run start_backend.bat in one terminal
echo 3. Run start_frontend.bat in another terminal
echo 4. Open http://localhost:3000 in your browser
echo.
echo For cloud deployment, see DEPLOYMENT_GUIDE.md
echo ========================================

pause