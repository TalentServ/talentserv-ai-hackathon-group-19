# Quick MCP Connection Test for Cursor

## 🎯 Your Situation:
- ✅ MCP server is RUNNING
- ✅ Tools are working
- ❌ Cursor is NOT using them

This means it's a **Cursor configuration issue**, not a server problem.

---

## 🚀 FASTEST FIX - Try This First:

### Step 1: Find Your Cursor Settings File

Press `Windows + R`, then paste:
```
%APPDATA%\Cursor\User\settings.json
```

Click OK to open the file.

### Step 2: Add This Configuration

If the file is EMPTY or has just `{}`, replace EVERYTHING with:

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

If the file ALREADY HAS content, just add the `"mcpServers"` part:

```json
{
  "existing.setting": "value",
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
2. **COMPLETELY CLOSE CURSOR** (X button)
3. Wait 5 seconds
4. **Reopen Cursor**

### Step 4: Test with Explicit Reference

In Cursor chat, type EXACTLY:

```
@travelmind What's the weather in London?
```

Or:

```
Use the TravelMind MCP server to check weather in Mumbai
```

---

## 🔍 Alternative Location for Config

If the above doesn't work, try this location instead:

**Workspace Settings:**

Create or edit this file:
```
C:\Users\Admin\Desktop\TravelMind\.cursor\settings.json
```

Add the same MCP configuration there.

---

## 🎯 What You Should See When It Works:

```
You: "@travelmind weather in Mumbai"

Cursor: 
[Calling MCP tool: get_weather]

🌤️ Weather in Mumbai:
- Temperature: 32°C
- Rain: 30%
- Humidity: 65%
...
```

---

## ❌ If You STILL See Web Search:

Try being VERY explicit:

```
Call the TravelMind MCP tool "generate_recommendation" with location "Mumbai"
```

Or:

```
Execute MCP function: get_weather("London")
```

---

## 🆘 Last Resort - Check Cursor Version:

MCP support might need a specific Cursor version. Check:
1. Help → About
2. Make sure you have Cursor version 0.40+ (or latest)

If your version is old, update Cursor first.

---

## 📝 Quick Diagnostic:

Run this from Command Prompt:

```cmd
cd C:\Users\Admin\Desktop\TravelMind
test_mcp_connection.bat
```

This will show you exactly what's configured and what's working.

---

**Try the settings.json configuration above first - that's the most common fix!** 🚀
