@echo off
echo.
echo ========================================
echo TravelMind MCP Server - Quick Test
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run example script
echo Running test script...
echo.
python example_usage.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If you see weather data above, everything is working!
echo.
echo Next: Run the MCP server with: run_server.bat
echo Or add to Cursor following the instructions in README.md
echo.
pause
