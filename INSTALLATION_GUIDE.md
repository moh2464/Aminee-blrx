# 📖 Installation & Setup Guide

Complete guide to setup and run the Free Fire Bot.

## 🖥️ Requirements

- Python 3.8+
- Google Chrome browser
- 2GB RAM
- Internet connection

## 📥 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/moh2464/Aminee-blrx.git
cd Aminee-blrx
```

### Step 2: Run Setup Script

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

### Step 3: Configure

Edit `.env` file:
```env
TEAM_CODE=123456
HEADLESS_MODE=False
MATCH_WAIT_TIME=25
LOOP_SLEEP_TIME=3
```

### Step 4: Run Bot
```bash
# Windows
run.bat

# Linux/macOS
./run.sh
```

## 🔧 Manual Setup

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run
```bash
python main.py
```

## 🚨 Troubleshooting

### Python Not Found
Install from https://www.python.org/

### Chrome Not Found
Install from https://www.google.com/chrome/

### Permission Denied (Linux/macOS)
```bash
chmod +x run.sh
```

### Timeout Errors
Increase `DRIVER_TIMEOUT` in `.env`

## 📊 Checking Logs
```bash
# View log file
tail -f bot.log

# Search for errors
grep ERROR bot.log
```

## 🛑 Stopping Bot
Press `Ctrl + C` in terminal

---

For more info, see README.md