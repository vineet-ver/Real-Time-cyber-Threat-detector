#!/bin/bash

# Cyber Threat Detector - Automated Setup Script
# This script automates the installation and setup process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🚨 CYBER THREAT DETECTOR - SETUP SCRIPT 🚨           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root for network monitoring
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Running as root - Good for network monitoring${NC}"
else
    echo -e "${YELLOW}⚠️  Not running as root - Some features may be limited${NC}"
    echo -e "${YELLOW}   Consider running with: sudo ./setup.sh${NC}"
fi

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check Python version
echo ""
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION found"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 not found. Installing..."
    sudo apt-get update && sudo apt-get install -y python3-pip
fi

# Create project directory structure
echo ""
print_info "Creating project structure..."
mkdir -p templates static logs
print_status "Directory structure created"

# Create virtual environment
echo ""
print_info "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_status "pip upgraded"

# Install dependencies
echo ""
print_info "Installing dependencies (this may take a few minutes)..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependencies installed"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Generate secret key
echo ""
print_info "Generating secret key..."
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
print_status "Secret key generated"

# Create .env file
echo ""
print_info "Creating .env file..."
cat > .env << EOF
# Environment Configuration
FLASK_ENV=development
SECRET_KEY=$SECRET_KEY

# Detection Thresholds
PORT_SCAN_THRESHOLD=10
DDOS_PACKET_THRESHOLD=1000
BRUTE_FORCE_THRESHOLD=5

# Time Windows (seconds)
PORT_SCAN_TIME_WINDOW=60
DDOS_TIME_WINDOW=10
BRUTE_FORCE_TIME_WINDOW=300

# Monitoring Settings
MONITOR_INTERVAL=2
MAX_STORED_THREATS=100

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/threat_detector.log
EOF
print_status ".env file created"

# Create .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    print_info "Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Application specific
*.db
*.sqlite
EOF
    print_status ".gitignore created"
fi

# Check required files
echo ""
print_info "Checking required files..."
REQUIRED_FILES=("app.py" "config.py" "threat_detector.py" "requirements.txt" "templates/dashboard.html")
ALL_FILES_PRESENT=true

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status "$file found"
    else
        print_error "$file not found!"
        ALL_FILES_PRESENT=false
    fi
done

if [ "$ALL_FILES_PRESENT" = false ]; then
    print_error "Some required files are missing. Please ensure all files are present."
    exit 1
fi

# Test import of key modules
echo ""
print_info "Testing Python dependencies..."
python3 -c "import flask; import flask_socketio; import psutil; import sklearn; print('All imports successful')" && \
    print_status "All dependencies can be imported" || \
    print_error "Some dependencies failed to import"

# Create systemd service file template (optional)
echo ""
read -p "Create systemd service file for auto-start? (y/n): " CREATE_SERVICE
if [[ $CREATE_SERVICE == "y" || $CREATE_SERVICE == "Y" ]]; then
    print_info "Creating systemd service file template..."
    
    CURRENT_DIR=$(pwd)
    USER=$(whoami)
    
    cat > threat-detector.service << EOF
[Unit]
Description=Cyber Threat Detector
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
Environment="PATH=$CURRENT_DIR/venv/bin"
EnvironmentFile=$CURRENT_DIR/.env
ExecStart=$CURRENT_DIR/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    print_status "Service file created: threat-detector.service"
    echo ""
    echo -e "${YELLOW}To install the service:${NC}"
    echo "  sudo cp threat-detector.service /etc/systemd/system/"
    echo "  sudo systemctl daemon-reload"
    echo "  sudo systemctl enable threat-detector"
    echo "  sudo systemctl start threat-detector"
fi

# Create run script
echo ""
print_info "Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
source .env
python app.py
EOF
chmod +x run.sh
print_status "Run script created: ./run.sh"

# Create test script shortcut
cat > test.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python test_detector.py "$@"
EOF
chmod +x test.sh
print_status "Test script created: ./test.sh"

# Final instructions
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ SETUP COMPLETE!                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${BLUE}Quick Start Commands:${NC}"
echo ""
echo "  🚀 Start the application:"
echo "     ./run.sh"
echo "     OR"
echo "     source venv/bin/activate && python app.py"
echo ""
echo "  🧪 Run tests:"
echo "     ./test.sh --demo"
echo ""
echo "  📊 Access dashboard:"
echo "     http://localhost:5000"
echo ""
echo "  📝 View logs:"
echo "     tail -f logs/threat_detector.log"
echo ""
echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "  • Network monitoring requires elevated privileges"
echo "  • Run with sudo for full functionality: sudo ./run.sh"
echo "  • Check .env file for configuration options"
echo "  • Default port is 5000, change in config.py if needed"
echo ""
echo -e "${GREEN}Happy threat hunting! 🎯${NC}"
echo ""