# Step-by-Step: Fix Cursor MCP Connection

## 🎯 Your Issue:
Cursor said: "I'm a coding assistant... I'm not able to help with personal travel decisions"

**This means:** Cursor is NOT connected to TravelMind MCP server.

---

## ✅ Fix in 5 Minutes:

### Step 1: Run Diagnostic Script

Open Command Prompt in TravelMind folder and run:
```cmd
cd C:\Users\Admin\Desktop\TravelMind
diagnose_cursor.bat
```

This will:
- ✅ Check if server is running
- ✅ Find your Cursor settings file
- ✅ Check if MCP is configured
- ✅ Open the file for you if needed

### Step 2: Add Configuration

When the diagnostic opens your settings file, add this:

```json
{
  "mcpServers": {
    "travelmind": {
      "command": "cmd.exe",
      "args": ["/c", "C:\\Users\\Admin\\Desktop\\TravelMind\\start_mcp.bat"],
      "env": {
        "OPENWEATHER_API_KEY": "your_openweather_api_key_here",
        "GEOAPIFY_API_KEY": "your_geoapify_api_key_here"
      }
    }
  }
}
```

**IMPORTANT:** 
- If file already has content, add `"mcpServers"` inside existing `{}`
- Don't delete existing settings!

### Step 3: Restart Cursor

1. Close ALL Cursor windows
2. Open Task Manager (`Ctrl+Shift+Esc`)
3. End any "Cursor" processes
4. Wait 5 seconds
5. Open Cursor fresh

### Step 4: Test with @mention

In Cursor chat, type:
```
@travelmind Should I visit Goa next week?
```

The `@travelmind` explicitly tells Cursor to use the MCP server.

---

## 🔍 If @travelmind Doesn't Work:

### Check 1: MCP in Command Palette
1. Press `Ctrl+Shift+P`
2. Type "MCP"
3. Do you see MCP-related commands?
   - ✅ YES → MCP is available
   - ❌ NO → Your Cursor version might not support MCP

### Check 2: Cursor Version
1. Help → About Cursor
2. Check version number
3. Need version 0.40 or higher for MCP

### Check 3: Settings Location
Try opening settings directly:
```
Windows + R
%APPDATA%\Cursor\User\settings.json
```

---

## 🆘 Still Not Working? Alternative Methods:

### Method A: Workspace Settings

Create this file:
```
C:\Users\Admin\Desktop\TravelMind\.vscode\settings.json
```

Add the MCP configuration there instead.

### Method B: Use Claude Desktop

If Cursor doesn't support MCP:
1. Download Claude Desktop app
2. Configure MCP in: `%APPDATA%\Claude\claude_desktop_config.json`
3. Use same configuration as above

### Method C: Explicit Tool Call

Try being VERY explicit:
```
Execute the MCP function "generate_recommendation" with parameter location="Goa"
```

---

## ✅ Success Indicators:

You'll know it's working when you see:

```
[Using TravelMind MCP tool: generate_recommendation]

✈️ Travel Recommendation for Goa:
✅ Yes, good time to visit!
📊 Confidence: 85%
🌤️ Weather: 32°C, 20% rain
...
```

Instead of:
```
I'm a coding assistant... I can't help with travel decisions
```

---

## 🚀 Quick Actions:

**RIGHT NOW, do these:**

1. Run: `diagnose_cursor.bat` ← START HERE
2. Add config to the file it shows you
3. Save (`Ctrl+S`)
4. Restart Cursor completely
5. Test: `@travelmind visit Goa`

**If that doesn't work:**
1. Check Cursor version (Help → About)
2. Update Cursor if old
3. Try workspace settings method
4. Or switch to Claude Desktop

---

Let me know what happens after you run the diagnostic script! 🎯
