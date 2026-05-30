
# 🎮 Free Fire Bot - Team Joining & Match Management

Automatic bot for Free Fire that joins teams and manages matches automatically with advanced error handling and configuration management.

## ✨ Features

### Core Features
- ✅ Automatic team joining with team code
- ✅ Match detection and automatic wait (25 seconds)
- ✅ Automatic match exit without app closure
- ✅ Team membership verification
- ✅ Continuous loop operation
- ✅ Comprehensive logging with timestamps
- ✅ Advanced error handling and recovery
- ✅ Fully configurable settings via `.env`

### Enhanced Features (V2.0)
- 🔄 Automatic retry logic for failed operations
- 🏥 Health checks for driver connection
- 🔐 Login support for Free Fire accounts
- 📊 Better logging with visual indicators
- 🚨 Stale element reference handling
- ⚙️ Multiple selector fallbacks for elements
- 🎯 Configuration validation
- 📁 Automatic logs directory creation

## 📋 Requirements

- Python 3.8+
- Google Chrome or Chromium browser
- ChromeDriver (auto-downloaded by webdriver-manager)
- Internet connection
- 2GB RAM minimum

## 🚀 Quick Start

### Windows
```bash
run.bat
```

### Linux/macOS
```bash
chmod +x run.sh
./run.sh
```

## 📖 Full Documentation

See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed setup instructions.

## ⚙️ Configuration

Edit `.env` file with your settings:

```env
# Your team code (REQUIRED)
TEAM_CODE=123456

# Run without GUI
HEADLESS_MODE=False

# Seconds to wait in match
MATCH_WAIT_TIME=25

# Sleep between iterations
LOOP_SLEEP_TIME=3

# Login credentials (optional)
FF_LOGIN_EMAIL=your_email@example.com
FF_LOGIN_PASSWORD=your_password
```

## 🎯 How It Works

```
1. Initialize WebDriver & Load Config
   ↓
2. Navigate to Free Fire Web App
   ↓
3. Login (if credentials provided)
   ↓
4. Join Team (with automatic retries)
   ↓
5. Enter Main Loop:
   ├─ Health Check (driver alive?)
   ├─ Check if in match
   │  ├─ YES: Wait X seconds → Exit match
   │  └─ NO: Continue
   ├─ Check if in team
   │  ├─ NO: Rejoin team with retries
   │  └─ YES: Continue
   └─ Sleep before next iteration
   ↓
6. Repeat Loop (Ctrl+C to stop)
```

## 📝 Logging

All activities logged to `logs/bot.log` with timestamps.

### View Logs
```bash
# Linux/macOS - Live tail
tail -f logs/bot.log

# Windows - View file
type logs/bot.log

# Search for errors
grep ERROR logs/bot.log
```

### Log Levels
Set `LOG_LEVEL` in `.env`:
- `DEBUG` - Detailed debug information
- `INFO` - General information (default)
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors

## 🛑 Stop Bot

Press `Ctrl + C` in terminal

## 🔧 Advanced Configuration

### Retry Settings
```env
# Maximum retries for joining team
MAX_RETRIES=3

# Delay between retries (seconds)
RETRY_DELAY=5
```

### Performance Tuning
```env
# WebDriver timeout (increase if slow internet)
DRIVER_TIMEOUT=10

# Chrome path (if auto-detection fails)
CHROME_PATH=/path/to/chrome
```

## 🐛 Troubleshooting

### Bot Crashes
- Check `logs/bot.log` for error messages
- Increase `DRIVER_TIMEOUT` in `.env`
- Ensure Chrome is installed

### Cannot Find Team Code Button
- The bot uses multiple fallback selectors
- If still not working, update XPath in code
- Check browser developer tools for element IDs

### Login Issues
- Leave `FF_LOGIN_EMAIL` and `FF_LOGIN_PASSWORD` empty to skip login
- Bot will continue without authentication

### Timeout Errors
```env
# Increase timeout (in .env)
DRIVER_TIMEOUT=20
```

### Permission Denied (Linux/macOS)
```bash
chmod +x run.sh
./run.sh
```

## 📊 Performance Metrics

- **Startup Time**: ~10-15 seconds
- **Match Detection**: Real-time
- **Memory Usage**: ~200-300MB
- **CPU Usage**: ~5-15% (varies by system)

## ⚠️ Important Notes

1. **Terms of Service**: Using bots may violate Free Fire's Terms of Service. Use at your own risk.
2. **Account Safety**: Use a secondary account if possible
3. **Rate Limiting**: The bot includes delays to avoid detection
4. **Monitoring**: Regularly check logs for issues

## 📞 Support

- 📖 Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- 🐛 Review `logs/bot.log` for detailed errors
- 💬 Open GitHub issue with logs attached
- 🔍 Enable `DEBUG` logging for more information

## 🔄 Update Log

### V2.0 (Current)
- Added Configuration class with validation
- Implemented retry logic with configurable attempts
- Added login support
- Improved error handling with fallback selectors
- Health checks for driver connection
- Better logging with visual indicators
- Created actual `.env` file
- Automatic logs directory creation

### V1.0
- Basic team joining
- Match detection
- Match exit functionality
- Comprehensive logging

## 📝 License

This project is provided as-is for educational purposes.

---

**Version**: 2.0.0  
**Author**: moh2464  
**Last Updated**: 2026-05-30  
**Status**: ✅ Production Ready