#!/bin/bash

# Cyber Threat Detector - Run Script
# This script activates the virtual environment and starts the application

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚨 Starting Cyber Threat Detector...${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Virtual environment not found!${NC}"
    echo -e "${BLUE}ℹ Running setup first...${NC}"
    
    if [ -f "setup.sh" ]; then
        chmod +x setup.sh
        ./setup.sh
    else
        echo -e "${RED}✗ setup.sh not found. Please run manually:${NC}"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${GREEN}✓${NC} Activating virtual environment..."
source venv/bin/activate

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo -e "${RED}✗ app.py not found!${NC}"
    echo "  Make sure you're in the correct directory"
    exit 1
fi

# Start the application
echo -e "${GREEN}✓${NC} Starting application..."
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Dashboard: http://localhost:5000${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the app
python app.py