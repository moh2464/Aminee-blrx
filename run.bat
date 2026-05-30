@echo off
REM Free Fire Bot Launcher - Windows

echo.
echo ╔════════════════════════════════════════╗
echo ║   Free Fire Bot - Launcher             ║
echo ╚════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Install from https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create venv
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate venv
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Check .env
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy .env.example .env
    echo ✅ Created .env - please edit it
    pause
    exit /b 0
)

echo.
echo ╔════════════════════════════════════════╗
echo ║   Starting Free Fire Bot...            ║
echo ╚════════════════════════════════════════╝
echo.

REM Run bot
python main.py

pause