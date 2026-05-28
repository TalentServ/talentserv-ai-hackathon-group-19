# TravelMind MCP - Cursor Configuration Guide

## ✅ Server Status: RUNNING
- Process ID: Running on port
- Tools: 8 available
- Resources: 5 available

---

## 🔧 Step-by-Step Setup for Cursor

### Step 1: Open Cursor MCP Settings

**Method A (Recommended):**
1. Open Cursor
2. Press `Ctrl + ,` (Settings)
3. Search for "MCP"
4. Click "Edit in settings.json" or find MCP configuration section

**Method B:**
1. Press `Ctrl + Shift + P` (Command Palette)
2. Type: "Preferences: Open User Settings (JSON)"
3. Add MCP configuration

**Method C:**
The config file is usually located at:
```
%APPDATA%\Cursor\User\settings.json
```
Or:
```
C:\Users\Admin\AppData\Roaming\Cursor\User\settings.json
```

### Step 2: Add This EXACT Configuration

**Copy and paste this into your Cursor settings:**

```json
{
  "mcpServers": {
    "travelmind": {
      "command": "cmd.exe",
      "args": [
        "/c",
        "C:\\Users\\Admin\\Desktop\\TravelMind\\start_mcp.bat"
      ],
      "env": {
        "OPENWEATHER_API_KEY": "your_openweather_api_key_here",
        "GEOAPIFY_API_KEY": "your_geoapify_api_key_here"
      }
    }
  }
}
```

**IMPORTANT:** If you already have other settings, add just the `"mcpServers"` section, don't replace everything!

### Step 3: Save and Restart Cursor

1. Save the settings file (`Ctrl + S`)
2. **Close Cursor completely** (not just the window)
3. **Reopen Cursor**
4. Wait 5-10 seconds for MCP to connect

### Step 4: Verify MCP is Connected

**Option A - Check MCP Status:**
1. Look at bottom-right of Cursor
2. You should see an MCP indicator or "travelmind" server listed

**Option B - Check Command Palette:**
1. Press `Ctrl + Shift + P`
2. Type "MCP"
3. Look for "MCP: List Tools" or similar
4. You should see TravelMind tools listed

### Step 5: Test with Explicit Tool Request

In Cursor chat, try this EXACT message:

```
@travelmind What's the weather in London?
```

Or more explicit:

```
Use the MCP tool "get_weather" to check weather in London
```

---

## 🚨 Common Issues & Fixes

### Issue 1: "MCP server not found"

**Fix:**
1. Check the path in config is correct:
   ```
   C:\\Users\\Admin\\Desktop\\TravelMind\\start_mcp.bat
   ```
2. Use double backslashes `\\` in JSON
3. Make sure the file exists at that location

**Verify:**
```cmd
dir C:\Users\Admin\Desktop\TravelMind\start_mcp.bat
```

### Issue 2: "Tools not appearing in Cursor"

**Fix:**
1. Make sure Cursor has MCP support enabled
2. Check Cursor version (needs recent version)
3. Try restarting Cursor as Administrator

### Issue 3: "Cursor still uses web search"

**Fix:**
1. Be very explicit in your prompts:
   - ❌ "What's the weather in Mumbai?"
   - ✅ "@travelmind weather in Mumbai"
   - ✅ "Use TravelMind tool to check Mumbai weather"
   
2. Mention "MCP tool" or "travelmind" in your query

### Issue 4: "Connection timeout"

**Fix:**
1. Make sure Python virtual environment is activated
2. Check if `start_mcp.bat` works manually:
   ```cmd
   cd C:\Users\Admin\Desktop\TravelMind
   start_mcp.bat
   ```
3. Look for error messages

---

## 🎯 Alternative: Create Cursor Extension File

If the above doesn't work, try creating a Cursor-specific extension file:

### Create: `.cursor/extensions/travelmind.json`

```json
{
  "name": "TravelMind",
  "version": "1.0.0",
  "mcp": {
    "command": "cmd.exe",
    "args": ["/c", "C:\\Users\\Admin\\Desktop\\TravelMind\\start_mcp.bat"],
    "env": {
      "OPENWEATHER_API_KEY": "your_openweather_api_key_here",
      "GEOAPIFY_API_KEY": "your_geoapify_api_key_here"
    }
  }
}
```

---

## 📝 Test Queries (Once Connected)

Try these in order:

### Test 1: Explicit MCP Tool Call
```
@travelmind get_weather("London")
```

### Test 2: Natural with Hint
```
Use the TravelMind MCP tool to check if I should visit Mumbai
```

### Test 3: Natural (should work after connection)
```
What's the weather in Tokyo?
```

### Test 4: Full Analysis
```
Give me complete travel analysis for Paris using TravelMind
```

---

## 🔍 Debug: Check if MCP is Loaded

### In Cursor Developer Console:
1. Press `Ctrl + Shift + I` (Developer Tools)
2. Go to Console tab
3. Type:
   ```javascript
   window.cursor.mcp.listServers()
   ```
4. Should show "travelmind" in the list

### Check Cursor Logs:
1. Open: `%APPDATA%\Cursor\logs\`
2. Look for files mentioning "MCP" or "travelmind"
3. Check for error messages

---

## ⚡ Quick Fix Script

Create this batch file to reset everything:

**reset_mcp.bat:**
```batch
@echo off
echo Stopping any running MCP servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq TravelMind*" 2>nul

echo Starting TravelMind MCP server...
cd C:\Users\Admin\Desktop\TravelMind
start "TravelMind MCP" cmd /k "venv\Scripts\activate && python main.py"

echo.
echo MCP server started!
echo Now restart Cursor and try again.
pause
```

Run this, then restart Cursor.

---

## 🎯 Expected Behavior When Working:

### You Type:
```
Should I visit Mumbai today?
```

### Cursor Should:
1. Show: "Using TravelMind MCP tool: generate_recommendation"
2. Display real-time data
3. Show charts inline
4. Mention PDF report path
5. NO web search indicator

### If You See Web Search Instead:
- ❌ "Searching the web for Mumbai weather..."
- ❌ No tool usage indicator

**Then MCP is NOT connected properly - follow steps above again.**

---

## 📞 Still Not Working?

If none of this works, try:

1. **Update Cursor to latest version**
2. **Check if Cursor supports MCP** (some versions don't)
3. **Try Claude Desktop instead** (native MCP support)
4. **Check Windows permissions** (run Cursor as Administrator)

---

## ✅ Success Checklist

- [ ] MCP server is running (check Task Manager for python.exe)
- [ ] Config file has correct path with double backslashes
- [ ] Cursor restarted after config change
- [ ] Can see "travelmind" in MCP status
- [ ] Test query uses tools instead of web search

Once all checked, it should work! 🚀
