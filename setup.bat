@echo off
REM Quick Start Script for SUN BREATHING Certificate Detection Platform
REM This script sets up and runs the complete system

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   🔥 SUN BREATHING | Certificate Detection Platform 🔥    ║
echo ║                                                            ║
echo ║   Quick Start Setup Script                               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python detected: 
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    pause
    exit /b 1
)

echo ✓ pip is ready

REM Install dependencies
echo.
echo 📦 Installing Python dependencies...
echo    This may take 2-3 minutes...
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✓ All dependencies installed successfully!

REM Initialize database
echo.
echo 🗄️  Initializing database with mock data...
python database.py

if %errorlevel% neq 0 (
    echo ⚠️  Database initialization had issues (may be already created)
)

echo.
echo ✓ Database ready!

REM Display next steps
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  ✓ SETUP COMPLETE!                        ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🚀 To start the server, run:
echo.
echo    python app.py
echo.
echo Then open your browser to: http://127.0.0.1:5000
echo.
echo 📚 For full documentation, see README.md
echo.
pause
