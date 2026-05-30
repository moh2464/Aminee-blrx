# 📖 Installation & Setup Guide

Complete step-by-step guide to setup and run the Free Fire Bot v2.0

## 🖥️ System Requirements

- **OS**: Windows 10/11, macOS 10.12+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: Minimum 2GB (4GB recommended)
- **Browser**: Google Chrome or Chromium installed
- **Internet**: Stable connection required

## 📥 Installation Steps

### Step 1: Clone Repository

```bash
# HTTPS
git clone https://github.com/moh2464/Aminee-blrx.git
cd Aminee-blrx

# OR SSH (if you have SSH key configured)
git clone git@github.com:moh2464/Aminee-blrx.git
cd Aminee-blrx
```

### Step 2: Run Automated Setup

The easiest way is to use the provided setup scripts:

#### Windows
```bash
run.bat
```

#### Linux/macOS
```bash
chmod +x run.sh
./run.sh
```

**What the scripts do:**
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Create `.env` file (if not exists)
- ✅ Create logs directory
- ✅ Run the bot

---

## 🔧 Manual Setup (Alternative)

If the scripts don't work, follow these steps:

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Bot

**Copy the example config:**
```bash
cp .env.example .env
```

**Edit `.env` with your settings:**
```bash
# Windows
notepad .env

# Linux/macOS
nano .env
```

**Essential settings:**
```env
TEAM_CODE=YOUR_TEAM_CODE_HERE    # Replace with actual team code
HEADLESS_MODE=False              # Set to True to hide browser
MATCH_WAIT_TIME=25               # Seconds to wait in match
LOOP_SLEEP_TIME=3                # Seconds between iterations
```

### Step 4: Run Bot

```bash
python main.py
```

---

## 🚀 Running the Bot

### First Time Setup
```bash
# Navigate to project directory
cd Aminee-blrx

# Windows - Use run.bat
run.bat

# Linux/macOS - Use run.sh
./run.sh
```

### Subsequent Runs (Windows)
```bash
venv\Scripts\activate
python main.py
```

### Subsequent Runs (Linux/macOS)
```bash
source venv/bin/activate
python main.py
```

---

## ⚙️ Configuration Guide

### Basic Configuration

**Required Settings:**
```env
TEAM_CODE=123456              # Your actual team code (REQUIRED)
```

**Optional Settings:**
```env
HEADLESS_MODE=False           # Hide browser window
MATCH_WAIT_TIME=25            # How long to wait in match
LOOP_SLEEP_TIME=3             # Pause between checks
```

### Advanced Configuration

**Performance:**
```env
DRIVER_TIMEOUT=10             # Increase if slow internet (10-20)
MAX_RETRIES=3                 # How many times to retry joining
RETRY_DELAY=5                 # Seconds between retry attempts
```

**Logging:**
```env
LOG_LEVEL=INFO                # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=bot.log              # Log file name
```

**Login (Optional):**
```env
FF_LOGIN_EMAIL=your_email@gmail.com      # Your game email
FF_LOGIN_PASSWORD=your_password           # Your game password
```

**Custom Chrome Path (if auto-detect fails):**
```env
# Windows
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe

# macOS
CHROME_PATH=/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome

# Linux
CHROME_PATH=/usr/bin/google-chrome
```

---

## 🚨 Troubleshooting

### Issue: "Python not found"

**Solution:**
1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt

**Verify:**
```bash
python --version
```

### Issue: "Chrome not found"

**Solution:**
1. Install Google Chrome from [google.com/chrome](https://www.google.com/chrome/)
2. If installed but not detected, set `CHROME_PATH` in `.env`

**Find Chrome path:**
- Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Linux: `/usr/bin/google-chrome` or `/snap/bin/chromium`

### Issue: "Permission denied" (Linux/macOS)

**Solution:**
```bash
chmod +x run.sh
./run.sh
```

### Issue: "Timeout errors"

**Solution:**
```env
# In .env, increase timeout
DRIVER_TIMEOUT=20   # Try 15-20 seconds
```

### Issue: "Module not found" errors

**Solution:**
```bash
# Activate virtual environment first
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Then reinstall requirements
pip install -r requirements.txt
```

### Issue: "Cannot find team code button"

**Solution:**
1. The bot has multiple selector fallbacks
2. Check the logs for which selector worked
3. Open browser DevTools (F12) to find the correct element ID/class
4. Contact support with screenshot

### Issue: Bot crashes immediately

**Solution:**
1. Check `logs/bot.log` for error messages
2. Ensure all required settings in `.env` are correct
3. Try increasing `DRIVER_TIMEOUT` to 15-20 seconds
4. Check internet connection

---

## 📊 Checking Logs

### View Recent Logs

**Linux/macOS:**
```bash
# Last 50 lines
tail -n 50 logs/bot.log

# Live tail (real-time)
tail -f logs/bot.log
```

**Windows:**
```bash
# View entire log
type logs/bot.log

# View with line numbers
more logs/bot.log
```

### Search Logs

**Find errors:**
```bash
grep ERROR logs/bot.log
```

**Find specific message:**
```bash
grep "team" logs/bot.log
```

---

## 🎯 Verification Checklist

After setup, verify everything works:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Chrome/Chromium installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip list | grep selenium`)
- [ ] `.env` file created with `TEAM_CODE` set
- [ ] Bot starts without errors (`python main.py`)
- [ ] Bot logs appear in console
- [ ] `logs/bot.log` file is created

---

## 🛑 Stopping the Bot

### Normal Stop
Press `Ctrl + C` in the terminal

### Force Stop
If Ctrl+C doesn't work:

**Windows:**
```bash
taskkill /IM python.exe /F
taskkill /IM chromedriver.exe /F
```

**Linux/macOS:**
```bash
pkill -f "python main.py"
pkill -f chromedriver
```

---

## 🔄 Updating Bot

To update to the latest version:

```bash
# Navigate to project directory
cd Aminee-blrx

# Pull latest changes
git pull origin main

# Reinstall dependencies (in case of changes)
pip install -r requirements.txt

# Run updated bot
python main.py
```

---

## 💡 Tips & Best Practices

### Performance
- Set `HEADLESS_MODE=True` for faster execution
- Use `LOOP_SLEEP_TIME=2` for more responsive bot
- Increase `DRIVER_TIMEOUT` on slow connections

### Monitoring
- Enable `LOG_LEVEL=DEBUG` for detailed logs
- Check logs regularly for errors
- Monitor CPU/RAM usage

### Safety
- Use secondary account if possible
- Don't run multiple instances
- Keep browser updated
- Monitor for account restrictions

### Troubleshooting
- Always check `logs/bot.log` first
- Enable DEBUG logging to see detailed info
- Test manually in browser if bot fails
- Report issues with full logs

---

## 📞 Getting Help

1. **Check Logs**: Review `logs/bot.log` for error messages
2. **Read Docs**: Check [README.md](README.md) for FAQ
3. **Verify Config**: Ensure `.env` settings are correct
4. **Test Manually**: Try joining team manually in browser
5. **Open Issue**: Report bug with logs and setup info

---

## 🔗 Useful Links

- [Python Installation](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/)
- [GitHub Repository](https://github.com/moh2464/Aminee-blrx)
- [Selenium Documentation](https://selenium.dev/documentation/)

---

**Version**: 2.0.0  
**Last Updated**: 2026-05-30  
**Status**: ✅ Up to Date