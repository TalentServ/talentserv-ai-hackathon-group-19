# Complete Installation Guide for Windows

## Step 1: Install Python

### Download and Install Python

1. **Open your web browser** and go to:
   ```
   https://www.python.org/downloads/
   ```

2. **Download the installer:**
   - Click the yellow button "Download Python 3.12.x" (latest version)
   - Save the installer file (e.g., `python-3.12.x-amd64.exe`)

3. **Run the installer:**
   - Double-click the downloaded installer
   - ⚠️ **CRITICAL**: Check the box ✅ "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation (takes 2-3 minutes)
   - Click "Close" when done

4. **Restart PowerShell/Terminal:**
   - Close any open PowerShell or Command Prompt windows
   - Open a new PowerShell window

5. **Verify Python is installed:**
   - Open PowerShell
   - Run: `python --version`
   - You should see: `Python 3.12.x`

   If you get an error:
   - You may need to restart your computer
   - Or Python wasn't added to PATH - reinstall and check the PATH box

## Step 2: Get API Keys

### OpenWeatherMap API Key

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (top right)
3. Fill in the form and create account
4. Verify your email
5. Log in and go to: https://home.openweathermap.org/api_keys
6. Copy your API key (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

### Geoapify API Key

1. Go to: https://www.geoapify.com/
2. Click "Get Started Free"
3. Create account with email
4. Verify your email
5. Log in and go to: https://myprojects.geoapify.com/
6. Click on your project → API keys
7. Copy your API key

## Step 3: Automated Setup

1. **Open PowerShell** in your project folder:
   - Right-click the `TravelMind` folder
   - Select "Open in Terminal" or "Open PowerShell here"

2. **Run the automated setup:**
   ```powershell
   .\setup.bat
   ```

3. **When prompted**, add your API keys to the `.env` file:
   ```env
   OPENWEATHER_API_KEY=your_actual_openweather_key_here
   GEOAPIFY_API_KEY=your_actual_geoapify_key_here
   ```
   - Replace the placeholder text with your actual keys
   - No quotes needed
   - Save and close the file

## Step 4: Test Installation

Run the test script:
```powershell
.\test_installation.bat
```

You should see:
- Weather data for Pune
- AQI information
- Tourist places
- Shopping list
- PDF and chart generation

## Step 5: Add to Cursor

1. **Open Cursor**

2. **Open MCP Settings:**
   - Press `Ctrl+Shift+P`
   - Type "MCP"
   - Select "MCP: Edit Configuration"

3. **Add TravelMind configuration:**
   ```json
   {
     "mcpServers": {
       "travelmind": {
         "command": "C:\\Users\\Admin\\Desktop\\TravelMind\\venv\\Scripts\\python.exe",
         "args": ["C:\\Users\\Admin\\Desktop\\TravelMind\\main.py"],
         "env": {
           "OPENWEATHER_API_KEY": "your_openweather_key",
           "GEOAPIFY_API_KEY": "your_geoapify_key"
         }
       }
     }
   }
   ```
   - Replace `your_openweather_key` with your actual key
   - Replace `your_geoapify_key` with your actual key
   - Use double backslashes `\\` in paths

4. **Save and restart Cursor**

## Step 6: Test in Cursor

Open a chat and ask:
```
"Should I visit Mumbai today? Give me a complete analysis."
```

Cursor will use TravelMind's MCP tools automatically!

## Troubleshooting

### "Python not found" after installation

1. Restart your computer
2. Run PowerShell as Administrator
3. Check if Python is in PATH:
   ```powershell
   $env:PATH -split ';' | Select-String python
   ```
4. If not found, add manually:
   - Search Windows for "Environment Variables"
   - Edit "Path" variable
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python312`
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts`

### "pip not found"

```powershell
python -m ensurepip --upgrade
```

### "Module not found" errors

```powershell
cd C:\Users\Admin\Desktop\TravelMind
venv\Scripts\activate
pip install -r requirements.txt
```

### API errors

- Check your API keys are correct in `.env`
- Verify keys are active on the API provider websites
- Check your internet connection
- Free tier has rate limits - wait a minute and retry

## Quick Commands Reference

```powershell
# Setup (run once)
.\setup.bat

# Test installation
.\test_installation.bat

# Run MCP server manually (optional)
.\run_server.bat

# Check Python
.\check_python.bat
```

## Need Help?

1. Check if Python is installed: `python --version`
2. Check if venv exists: `dir venv`
3. Check if dependencies installed: `venv\Scripts\pip list`
4. Review logs in the `logs/` folder
5. Open an issue on GitHub with error details

---

**After completing all steps, you're ready to use TravelMind with Cursor!** 🎉
