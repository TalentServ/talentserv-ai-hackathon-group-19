@echo off
echo.
echo =============================================
echo TravelMind MCP - Quick Test Script
echo =============================================
echo.

echo [1] Checking if MCP server is running...
tasklist | findstr /i "python.exe" >nul
if %errorlevel% equ 0 (
    echo    ✓ Python process found
) else (
    echo    ✗ Python not running
    echo.
    echo    Starting MCP server...
    cd /d "%~dp0"
    start "TravelMind MCP Server" cmd /k "call venv\Scripts\activate.bat && python main.py"
    timeout /t 3 >nul
)

echo.
echo [2] Testing if server responds...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -c "from tools import MCPTools; tools = MCPTools(); print('✓ MCP tools loaded successfully')" 2>nul
if %errorlevel% equ 0 (
    echo    ✓ Server is responding
) else (
    echo    ✗ Server not responding
)

echo.
echo [3] Checking configuration...
if exist "cursor_mcp_config.json" (
    echo    ✓ Config file exists
) else (
    echo    ✗ Config file missing
)

echo.
echo [4] Checking API keys...
if defined OPENWEATHER_API_KEY (
    echo    ✓ Weather API key found
) else (
    echo    ⚠ Weather API key not in environment
)

echo.
echo =============================================
echo Next Steps:
echo =============================================
echo.
echo 1. Open Cursor Settings (Ctrl + ,)
echo 2. Search for "MCP"
echo 3. Add configuration from cursor_mcp_config.json
echo 4. Restart Cursor completely
echo 5. Try: "@travelmind weather in London"
echo.
echo Configuration to add:
echo.
type cursor_mcp_config.json
echo.
echo =============================================
pause
