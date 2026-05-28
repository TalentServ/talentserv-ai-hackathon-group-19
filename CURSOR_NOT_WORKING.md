# CRITICAL: Cursor MCP Configuration Not Working

## The Problem:
- MCP server IS running ✅
- Cursor is NOT using it ❌
- Cursor responds as a coding assistant instead of using travel tools

## The Solution:

### Step 1: Find Cursor's Config Location

Cursor MCP config can be in several places. Try these in order:

#### Option A: Cursor Settings (MOST COMMON)
1. Open Cursor
2. Press `Ctrl + Shift + P`
3. Type: "Preferences: Open User Settings (JSON)"
4. Click it

#### Option B: Direct File Access
Press `Windows + R` and try these paths one by one:

**Path 1:**
```
%APPDATA%\Cursor\User\settings.json
```

**Path 2:**
```
C:\Users\Admin\AppData\Roaming\Cursor\User\settings.json
```

**Path 3 (Workspace):**
```
C:\Users\Admin\Desktop\TravelMind\.vscode\settings.json
```

### Step 2: Add MCP Configuration

Once you open the settings file, add this:

**If file is EMPTY or just `{}`:**
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

**If file ALREADY HAS CONTENT:**
Add the `"mcpServers"` block inside the existing curly braces:

```json
{
  "existing.setting": "value",
  "another.setting": "value",
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

### Step 3: Save and Restart

1. Save the file (`Ctrl + S`)
2. **Close Cursor COMPLETELY** (not just window - use Task Manager if needed)
3. Wait 5 seconds
4. Open Cursor again

### Step 4: Verify MCP is Loaded

Look for one of these indicators:
- Bottom status bar showing "MCP" or "travelmind"
- Settings showing MCP servers
- Command palette has MCP options

### Step 5: Test Again

Try EXACTLY this in Cursor chat:
```
@travelmind Should I visit Goa next week?
```

Or be very explicit:
```
Use the TravelMind MCP tool to analyze if I should visit Goa next week
```

---

## Alternative: Check if Cursor Supports MCP

Some Cursor versions don't support MCP yet.

**Check your version:**
1. Help → About Cursor
2. Look for version number
3. MCP requires Cursor 0.40+ or newer

**If your version is old:**
- Update Cursor to latest version
- OR use Claude Desktop (native MCP support)

---

## Quick Test Script

I'll create a script to verify your configuration:
