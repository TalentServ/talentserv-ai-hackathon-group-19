@echo off
echo.
echo ========================================
echo TravelMind MCP Server - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python first:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.11 or higher
    echo 3. Run installer and CHECK "Add Python to PATH"
    echo 4. Run this script again after installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env >nul
    echo.
    echo [ACTION REQUIRED] Please edit .env file and add your API keys:
    echo - OPENWEATHER_API_KEY=your_key_here
    echo - GEOAPIFY_API_KEY=your_key_here
    echo.
    notepad .env
)

REM Create virtual environment
echo [STEP 1] Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment and install dependencies
echo [STEP 2] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create output directories
echo [STEP 3] Creating output directories...
if not exist "reports" mkdir reports
if not exist "charts" mkdir charts
if not exist "logs" mkdir logs
echo Directories created
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure your API keys are in .env file
echo 2. Run: test_installation.bat
echo 3. If test passes, run: run_server.bat
echo.
pause
