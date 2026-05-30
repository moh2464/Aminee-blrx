@echo off
REM Free Fire Bot - Windows Startup Script
REM This script handles virtual environment setup and bot execution

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════╗
echo ║   Free Fire Bot - Automated Setup      ║
echo ║   Version 2.0                          ║
echo ╚════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 📥 Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🚀 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip -q
echo ✅ pip upgraded
echo.

REM Install requirements
if exist "requirements.txt" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt -q
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
) else (
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)
echo.

REM Create logs directory
if not exist "logs" (
    echo 📁 Creating logs directory...
    mkdir logs
    echo ✅ Logs directory created
) else (
    echo ✅ Logs directory already exists
)
echo.

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found
    if exist ".env.example" (
        echo 📝 Creating .env from .env.example...
        copy .env.example .env >nul
        echo ✅ .env file created
        echo 📋 Please edit .env and set TEAM_CODE before running
    ) else (
        echo ❌ .env.example not found
    )
    echo.
    pause
) else (
    echo ✅ .env file found
    echo.
)

REM Run the bot
echo 🤖 Starting Free Fire Bot...
echo ─────────────────────────────────
echo.
python main.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ─────────────────────────────────
    echo ❌ Bot encountered an error
    echo 📖 Check logs/bot.log for details
) else (
    echo.
    echo ─────────────────────────────────
    echo ✅ Bot closed successfully
)

echo.
pause