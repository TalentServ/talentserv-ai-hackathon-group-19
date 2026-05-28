@echo off
echo.
echo ========================================
echo TravelMind MCP Server - Starting...
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the server
echo Starting MCP server...
echo Press Ctrl+C to stop the server
echo.
python main.py

pause
