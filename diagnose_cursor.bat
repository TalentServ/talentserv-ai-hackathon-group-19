@echo off
echo.
echo ====================================================
echo Cursor MCP Configuration Diagnostic
echo ====================================================
echo.

echo [1] Checking if MCP server is running...
tasklist | findstr /i "python.exe" >nul
if %errorlevel% equ 0 (
    echo    ✓ MCP server IS running
) else (
    echo    ✗ MCP server NOT running
    echo    Run: start_mcp.bat
    pause
    exit /b 1
)

echo.
echo [2] Looking for Cursor settings files...
echo.

set FOUND=0

if exist "%APPDATA%\Cursor\User\settings.json" (
    echo    ✓ Found: %APPDATA%\Cursor\User\settings.json
    set SETTINGS_FILE=%APPDATA%\Cursor\User\settings.json
    set FOUND=1
) else (
    echo    ✗ Not found: %APPDATA%\Cursor\User\settings.json
)

if exist "C:\Users\%USERNAME%\AppData\Roaming\Cursor\User\settings.json" (
    echo    ✓ Found: C:\Users\%USERNAME%\AppData\Roaming\Cursor\User\settings.json
    if %FOUND%==0 (
        set SETTINGS_FILE=C:\Users\%USERNAME%\AppData\Roaming\Cursor\User\settings.json
        set FOUND=1
    )
) else (
    echo    ✗ Not found: C:\Users\%USERNAME%\AppData\Roaming\Cursor\User\settings.json
)

echo.
if %FOUND%==1 (
    echo [3] Checking if MCP is configured...
    findstr /i "mcpServers" "%SETTINGS_FILE%" >nul
    if %errorlevel% equ 0 (
        echo    ✓ MCP configuration FOUND in settings
        echo.
        echo    Your configuration:
        findstr /i /c:"mcpServers" /c:"travelmind" /c:"command" "%SETTINGS_FILE%"
    ) else (
        echo    ✗ MCP configuration NOT FOUND
        echo.
        echo    You need to add MCP configuration!
        echo.
        echo    File to edit: %SETTINGS_FILE%
        echo.
        echo    Press any key to open the file...
        pause >nul
        notepad "%SETTINGS_FILE%"
        echo.
        echo    Copy this configuration:
        echo.
        type cursor_mcp_config.json
        echo.
        echo    Then restart Cursor!
    )
) else (
    echo    ✗ Could not find Cursor settings file
    echo.
    echo    Cursor might not be installed or using different location.
    echo.
    echo    Try these steps:
    echo    1. Open Cursor
    echo    2. Press Ctrl+Shift+P
    echo    3. Type: "Preferences: Open User Settings (JSON)"
    echo    4. Add the configuration from cursor_mcp_config.json
)

echo.
echo ====================================================
echo [4] Configuration to add:
echo ====================================================
echo.
type cursor_mcp_config.json
echo.
echo ====================================================
echo.
echo Next Steps:
echo 1. Copy the configuration above
echo 2. Add it to Cursor settings.json
echo 3. Save and restart Cursor COMPLETELY
echo 4. Test: "@travelmind should I visit Goa?"
echo.
pause
