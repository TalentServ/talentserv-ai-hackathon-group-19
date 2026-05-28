@echo off
echo.
echo Checking Python installation...
echo ================================
echo.

python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo.
echo Python is installed successfully!
echo.

python -m pip --version
if %errorlevel% neq 0 (
    echo [WARNING] pip is not available
) else (
    echo pip is available!
)

echo.
echo ================================
echo Installation check complete!
pause
