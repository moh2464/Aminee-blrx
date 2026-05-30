# 🎮 Free Fire Bot - Team Joining & Match Management

Automatic bot for Free Fire that joins teams and manages matches automatically.

## ✨ Features

- ✅ Automatic team joining with team code
- ✅ Match detection and 25-second wait
- ✅ Automatic match exit without app closure
- ✅ Team membership verification
- ✅ Continuous loop operation
- ✅ Comprehensive logging
- ✅ Error handling and recovery
- ✅ Configurable settings

## 📋 Requirements

- Python 3.8+
- Google Chrome or Chromium browser
- ChromeDriver (auto-downloaded)
- Internet connection

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

## 🎯 How It Works

```
1. Initialize WebDriver
   ↓
2. Join Team (using team code)
   ↓
3. Enter Main Loop:
   ├─ Check if in match
   │  ├─ YES: Wait 25 seconds → Exit match
   │  └─ NO: Continue
   ├─ Check if in team
   │  ├─ NO: Rejoin team
   │  └─ YES: Continue
   └─ Sleep 3 seconds
   ↓
4. Repeat Loop
```

## ⚙️ Configuration

Edit `.env` file:

```env
TEAM_CODE=123456              # Your team code
HEADLESS_MODE=False           # Run without GUI
MATCH_WAIT_TIME=25            # Seconds to wait in match
LOOP_SLEEP_TIME=3             # Sleep between iterations
```

## 📝 Logging

All activities logged to `bot.log` and console.

View logs:
```bash
# Linux/macOS
tail -f bot.log

# Windows
type bot.log
```

## 🛑 Stop Bot

Press `Ctrl + C` in terminal

## ⚠️ Disclaimer

Using bots may violate Free Fire's Terms of Service. Use at your own risk. Not responsible for account suspension or ban.

## 📞 Support

- 📖 Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- 🐛 Review `bot.log` for errors
- 💬 Open GitHub issue

---

**Version**: 1.0.0  
**Author**: moh2464  
**Last Updated**: 2026-05-30