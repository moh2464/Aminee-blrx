#!/bin/bash

# Free Fire Bot - Linux/macOS Startup Script
# This script handles virtual environment setup and bot execution

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
echo ""
echo "╔════════════════════════════════════════╗"
echo "║   Free Fire Bot - Automated Setup      ║"
echo "║   Version 2.0                          ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo -e "${YELLOW}📥 Please install Python 3.8+ using:${NC}"
    echo "   macOS: brew install python3"
    echo "   Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo -e "${GREEN}✅ Python found:${NC}"
python3 --version
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed${NC}"
    echo -e "${YELLOW}📥 Please install pip3:${NC}"
    echo "   macOS: brew install python3"
    echo "   Ubuntu/Debian: sudo apt-get install python3-pip"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}🔧 Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}🚀 Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    read -p "Press Enter to exit..."
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
python -m pip install --upgrade pip -q
echo -e "${GREEN}✅ pip upgraded${NC}"
echo ""

# Install requirements
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}📥 Installing dependencies...${NC}"
    pip install -r requirements.txt -q
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    read -p "Press Enter to exit..."
    exit 1
fi
echo ""

# Create logs directory
if [ ! -d "logs" ]; then
    echo -e "${BLUE}📁 Creating logs directory...${NC}"
    mkdir -p logs
    echo -e "${GREEN}✅ Logs directory created${NC}"
else
    echo -e "${GREEN}✅ Logs directory already exists${NC}"
fi
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    if [ -f ".env.example" ]; then
        echo -e "${BLUE}📝 Creating .env from .env.example...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✅ .env file created${NC}"
        echo -e "${YELLOW}📋 Please edit .env and set TEAM_CODE before running${NC}"
    else
        echo -e "${RED}❌ .env.example not found${NC}"
    fi
    echo ""
    read -p "Press Enter to continue..."
else
    echo -e "${GREEN}✅ .env file found${NC}"
    echo ""
fi

# Run the bot
echo -e "${BLUE}🤖 Starting Free Fire Bot...${NC}"
echo "─────────────────────────────────"
echo ""
python main.py

# Check exit code
EXIT_CODE=$?
echo ""
echo "─────────────────────────────────"
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}❌ Bot encountered an error${NC}"
    echo -e "${YELLOW}📖 Check logs/bot.log for details${NC}"
else
    echo -e "${GREEN}✅ Bot closed successfully${NC}"
fi
echo ""

# Optional: Keep terminal open
if [ "$1" != "--no-pause" ]; then
    read -p "Press Enter to exit..."
fi