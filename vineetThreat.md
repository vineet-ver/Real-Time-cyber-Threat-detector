🚀 Complete Step-by-Step Guide to Run Your Cyber Threat Detector
I'll guide you through every single step from setup to running the application. Let's start!

📋 STEP 1: Verify Your Project Structure
First, make sure all your files are organized correctly:
cyber-threat-detector/
├── app.py
├── config.py
├── threat_detector.py
├── test_detector.py
├── requirements.txt
├── setup.sh
├── run.sh
├── test.sh
├── Dockerfile
├── docker-compose.yml
├── README.md
├── DEPLOYMENT.md
├── PROJECT_SUMMARY.md
├── QUICK_REFERENCE.md
└── templates/
    └── dashboard.html
Action: Open your terminal/command prompt and navigate to your project folder:
bashcd path/to/cyber-threat-detector

🎯 CHOOSE YOUR METHOD (Pick One)
You have 3 options to run this app:
Option A: Simple Method (Without Docker) ⭐ RECOMMENDED FOR BEGINNERS
Option B: Docker Method 🐳 RECOMMENDED FOR PRODUCTION
Option C: Manual Method 🔧 FOR LEARNING

🟢 OPTION A: SIMPLE METHOD (Automated Setup)
This is the easiest way to get started!
Step A1: Make Scripts Executable (Linux/Mac Only)
bashchmod +x setup.sh run.sh test.sh
Windows Users: Skip this step and use bash setup.sh instead.

Step A2: Run the Automated Setup Script
On Linux/Mac:
bash./setup.sh
On Windows (Git Bash or WSL):
bashbash setup.sh
What this does:

✅ Creates virtual environment
✅ Installs all dependencies
✅ Generates secret key
✅ Creates .env file
✅ Sets up directory structure

Wait for: "✅ SETUP COMPLETE!" message (takes 2-5 minutes)

Step A3: Start the Application
On Linux/Mac:
bash./run.sh
On Windows:
bashbash run.sh
OR Start Manually:
bash# Activate virtual environment
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Run the app
python app.py

Step A4: Access the Dashboard

Open your web browser
Go to: http://localhost:5000
You should see: The Cyber Threat Detector Dashboard! 🎉

If you see the dashboard, skip to Step A6!

Step A5: Test the Application
In a NEW terminal window, run the test suite:
On Linux/Mac:
bash./test.sh --demo
On Windows:
bashbash test.sh --demo
What happens:

Simulates port scans
Simulates DDoS attacks
Generates test threats
Shows results on dashboard


Step A6: Monitor in Real-Time
Watch your dashboard at http://localhost:5000 to see:

📊 Threat counters increasing
📈 Chart updating in real-time
🚨 New threats appearing in the feed


Step A7: Stop the Application
Press Ctrl + C in the terminal where the app is running.

🐳 OPTION B: DOCKER METHOD
Perfect if you have Docker installed!
Prerequisites Check
bash# Check if Docker is installed
docker --version

# Check if Docker Compose is installed
docker-compose --version
Don't have Docker?

Download from: https://www.docker.com/products/docker-desktop
Install Docker Desktop for your OS
Restart your computer after installation


Step B1: Verify Docker is Running
On Windows/Mac:

Open Docker Desktop application
Wait for "Docker Desktop is running" message
Look for the whale icon in your system tray

On Linux:
bashsudo systemctl start docker
sudo systemctl status docker

Step B2: Build the Docker Image
Open terminal in your project folder:
bashdocker build -t threat-detector .
Wait for: "Successfully built" message (takes 3-10 minutes first time)
Troubleshooting:

If you get "permission denied": Run sudo docker build -t threat-detector .
If you get "Docker daemon not running": Start Docker Desktop


Step B3: Run with Docker Compose (EASIEST)
bashdocker-compose up -d
The -d flag runs it in background (detached mode)
What this does:

✅ Creates container
✅ Sets up networking
✅ Starts the application
✅ Runs on port 5000


Step B4: Verify Container is Running
bashdocker-compose ps
```

**You should see:**
```
NAME                    STATUS
cyber-threat-detector   Up

Step B5: View Logs
bashdocker-compose logs -f
Press Ctrl + C to stop viewing logs (app keeps running)

Step B6: Access the Dashboard

Open browser
Go to: http://localhost:5000
Dashboard should load! 🎉


Step B7: Stop the Docker Container
bashdocker-compose down
To restart:
bashdocker-compose up -d

Step B8: Alternative - Run Without Docker Compose
bash# Build (if not done already)
docker build -t threat-detector .

# Run the container
docker run -d \
  --name threat-detector \
  --network host \
  -p 5000:5000 \
  threat-detector

# View logs
docker logs -f threat-detector

# Stop container
docker stop threat-detector

# Remove container
docker rm threat-detector

🔧 OPTION C: MANUAL METHOD (Step-by-Step)
For complete control and learning!
Step C1: Install Python
Check Python version:
bashpython3 --version
Need: Python 3.8 or higher
Don't have Python?

Download: https://www.python.org/downloads/
Install (check "Add Python to PATH" on Windows)
Verify: python3 --version


Step C2: Create Virtual Environment
bash# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# You should see (venv) in your terminal prompt

Step C3: Upgrade pip
bashpip install --upgrade pip

Step C4: Install Dependencies
bashpip install -r requirements.txt
Wait for: All packages to install (2-5 minutes)
If you get errors:
bash# Try installing individually
pip install Flask==3.0.0
pip install flask-socketio==5.3.5
pip install scikit-learn==1.3.2
pip install pandas==2.1.4
pip install numpy==1.26.2
pip install psutil==5.9.6

Step C5: Create templates Directory
bashmkdir -p templates
Verify dashboard.html is inside the templates folder.

Step C6: Create .env File
Create a file named .env in your project root:
bash# Create the file
touch .env      # Linux/Mac
type nul > .env # Windows

# Edit with your text editor and add:
Add this content to .env:
envFLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this
PORT_SCAN_THRESHOLD=10
DDOS_PACKET_THRESHOLD=1000
MONITOR_INTERVAL=2

Step C7: Generate Secret Key (Optional but Recommended)
bash# Generate a random secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
Copy the output and replace your-super-secret-key-change-this in .env

Step C8: Create logs Directory
bashmkdir -p logs

Step C9: Verify File Structure
bash# Linux/Mac
ls -la

# Windows
dir
You should have:

✅ app.py
✅ config.py
✅ threat_detector.py
✅ requirements.txt
✅ templates/dashboard.html
✅ .env
✅ venv/ (folder)
✅ logs/ (folder)


Step C10: Run the Application
bashpython app.py
OR with admin privileges (for full network access):
Linux/Mac:
bashsudo -E python app.py
```

### **Windows:**
- Right-click Command Prompt
- Select "Run as Administrator"
- Navigate to project folder
- Run: `python app.py`

---

## **Step C11: Verify It's Running**

**You should see output like:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit

Step C12: Open Dashboard

Open browser
Go to: http://localhost:5000
See the dashboard! 🎉


Step C13: Test the Application
Open a NEW terminal, activate venv, and run:
bash# Activate venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Run tests
python test_detector.py --demo

🎮 USING THE APPLICATION
Dashboard Features:
1. Top Control Buttons:

▶ Start Monitor - Begins network monitoring
⏸ Stop Monitor - Pauses monitoring

2. Statistics Cards:

Port Scans Detected - Count of scanning attempts
DDoS Patterns - Potential DDoS attacks
Suspicious Traffic - ML-detected anomalies
Active Connections - Current network connections

3. Threat Timeline Chart:

Real-time graph showing threat activity
Updates automatically

4. Recent Threats Panel:

Live feed of detected threats
Color-coded by severity
Shows timestamp and details

5. Active Connections Panel:

Lists current network connections
Shows IP addresses and port counts


Testing the Detection:
Method 1: Automated Test Suite
bash# Interactive menu
python test_detector.py

# Full demo
python test_detector.py --demo

# Port scan simulation
python test_detector.py --port-scan

# DDoS simulation
python test_detector.py --ddos
Method 2: Manual cURL Tests
bash# Get current stats
curl http://localhost:5000/api/stats

# Get threats
curl http://localhost:5000/api/threats

# Scan an IP
curl http://localhost:5000/api/scan/127.0.0.1

🔍 TROUBLESHOOTING
Problem: "Port 5000 already in use"
Solution:
bash# Find what's using port 5000
lsof -i :5000          # Linux/Mac
netstat -ano | findstr :5000    # Windows

# Kill the process
kill -9 <PID>          # Linux/Mac
taskkill /PID <PID> /F # Windows

# Or use a different port
export PORT=8080
python app.py

Problem: "Permission denied" when running
Solution:
bash# Run with sudo (Linux/Mac)
sudo -E python app.py

# Run as Administrator (Windows)
# Right-click terminal → Run as Administrator

Problem: "Module not found" errors
Solution:
bash# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

Problem: Dashboard not loading
Check:

Is the app running? (check terminal for errors)
Correct URL? (http://localhost:5000)
Firewall blocking? (temporarily disable and test)
Check browser console (F12) for errors


Problem: Docker won't start
Solution:
bash# Make sure Docker is running
docker ps

# If error, start Docker Desktop or service
sudo systemctl start docker  # Linux

# Check Docker logs
docker-compose logs
```

---

# 📊 **WHAT TO EXPECT**

## **When App Starts:**
```
✓ Virtual environment activated
✓ Dependencies loaded
✓ Threat monitor started
✓ Flask server running on port 5000
✓ WebSocket connection active
On Dashboard:

Real-time statistics updating every 2-3 seconds
Green pulsing indicator showing "System Online"
Charts rendering and updating
Connection list populating

When Running Tests:

Threats appearing in the feed
Counters incrementing
Charts showing activity spikes
Color-coded threat alerts


✅ SUCCESS CHECKLIST

 Project files copied to folder
 Python 3.8+ installed
 Virtual environment created
 Dependencies installed
 .env file created
 App running without errors
 Dashboard accessible at http://localhost:5000
 Statistics showing on dashboard
 Tests successfully simulate threats
 Real-time updates working


🎯 NEXT STEPS

Experiment with the test suite
Customize detection thresholds in config.py
Deploy to cloud platform (see DEPLOYMENT.md)
Extend with your own detection algorithms
Integrate with alerting systems