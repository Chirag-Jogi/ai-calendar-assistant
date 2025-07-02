@echo off
REM AI Appointment Assistant - Quick Setup Script (Windows)
REM Run this after cloning the repository

echo 🤖 AI Appointment Assistant - Setup Script
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip found

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Copy environment template
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your actual API keys.
) else (
    echo ℹ️  .env file already exists.
)

REM Create credentials directory
if not exist config\credentials mkdir config\credentials

echo.
echo 🚀 Setup Complete!
echo.
echo Next steps:
echo 1. Edit .env file with your Groq API key
echo 2. Add your Google service account JSON to config\credentials\service_account.json
echo 3. Run: streamlit run streamlit_app.py
echo.
echo For detailed instructions, see README.md
pause
