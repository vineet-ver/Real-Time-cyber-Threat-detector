# 🚀 Quick Reference Guide - Cyber Threat Detector

## ⚡ Quick Start

```bash
# Setup (one-time)
chmod +x setup.sh && ./setup.sh

# Run application
./run.sh
# OR
source venv/bin/activate && python app.py

# Run with admin privileges (recommended)
sudo ./run.sh
```

## 🎮 Common Commands

### Development

```bash
# Activate virtual environment
source venv/bin/activate              # Linux/Mac
venv\Scripts\activate                 # Windows

# Run in development mode
export FLASK_ENV=development
python app.py

# Run with debug mode
export FLASK_DEBUG=True
python app.py

# View logs
tail -f logs/threat_detector.log
```

### Testing

```bash
# Interactive test menu
./test.sh

# Run full demo
./test.sh --demo

# Specific tests
./test.sh --port-scan
./test.sh --ddos
./test.sh --stress 10 5  # 10 seconds, 5 threads

# API tests
./test.sh --test
```

### Docker

```bash
# Build image
docker build -t threat-detector .

# Run container
docker run -d -p 5000:5000 --name threat-detector threat-detector

# With Docker Compose
docker-compose up -d          # Start
docker-compose logs -f        # View logs
docker-compose down           # Stop
docker-compose restart        # Restart
```

### Deployment

```bash
# Render
render blueprint launch

# Railway
railway up

# Heroku
git push heroku main

# Production with Gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

## 🔌 API Endpoints

### Dashboard
```
GET  /                      Main dashboard interface
```

### Threats
```bash
# Get all threats
GET  /api/threats

# Example response
[
  {
    "type": "port_scan",
    "severity": "high",
    "source_ip": "192.168.1.100",
    "details": "Port scan detected: 15 unique ports",
    "timestamp": "2025-10-16T10:30:00"
  }
]
```

### Statistics
```bash
# Get current stats
GET  /api/stats

# Example response
{
  "attack_stats": {
    "port_scan": 5,
    "ddos": 2,
    "suspicious_traffic": 10,
    "unauthorized_access": 0
  },
  "active_connections": 25,
  "total_threats": 17
}
```

### Connections
```bash
# Get active connections
GET  /api/connections

# Example response
[
  {
    "ip": "192.168.1.100",
    "port_count": 3,
    "ports": [80, 443, 8080]
  }
]
```

### IP Scanning
```bash
# Scan specific IP
GET  /api/scan/<ip>

# Example
GET  /api/scan/192.168.1.100

# Response
{
  "ip": "192.168.1.100",
  "hostname": "device.local",
  "status": "active"
}
```

### Monitor Control
```bash
# Start monitoring
POST /api/monitor/start

# Stop monitoring
POST /api/monitor/stop

# Response
{"status": "started"} or {"status": "stopped"}
```

## 🧪 cURL Examples

```bash
# Get stats
curl http://localhost:5000/api/stats

# Get threats (formatted)
curl http://localhost:5000/api/threats | python -m json.tool

# Start monitor
curl -X POST http://localhost:5000/api/monitor/start

# Scan IP
curl http://localhost:5000/api/scan/127.0.0.1

# Get connections
curl http://localhost:5000/api/connections
```

## 🐍 Python API Usage

```python
import requests

BASE_URL = "http://localhost:5000"

# Get statistics
response = requests.get(f"{BASE_URL}/api/stats")
stats = response.json()
print(f"Total threats: {stats['total_threats']}")

# Get threats
response = requests.get(f"{BASE_URL}/api/threats")
threats = response.json()
for threat in threats:
    print(f"{threat['type']}: {threat['details']}")

# Start monitoring
response = requests.post(f"{BASE_URL}/api/monitor/start")
print(response.json())

# Scan IP
ip = "192.168.1.1"
response = requests.get(f"{BASE_URL}/api/scan/{ip}")
print(response.json())
```

## ⚙️ Configuration Quick Reference

### config.py Values

```python
# Detection Thresholds
PORT_SCAN_THRESHOLD = 10          # ports
DDOS_PACKET_THRESHOLD = 1000      # packets/sec
BRUTE_FORCE_THRESHOLD = 5         # attempts

# Time Windows
PORT_SCAN_TIME_WINDOW = 60        # seconds
DDOS_TIME_WINDOW = 10             # seconds
BRUTE_FORCE_TIME_WINDOW = 300     # seconds

# Monitoring
MONITOR_INTERVAL = 2              # seconds
MAX_STORED_THREATS = 100          # count
```

### Environment Variables

```bash
# Set in .env or export
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export PORT_SCAN_THRESHOLD=15
export DDOS_PACKET_THRESHOLD=2000
export MONITOR_INTERVAL=3
```

## 🔍 Threat Types

| Type | Description | Severity |
|------|-------------|----------|
| `port_scan` | Multiple ports accessed from single IP | High |
| `ddos` | Unusual traffic volume spike | Critical |
| `suspicious_traffic` | ML-detected anomaly | Medium |
| `suspicious_port` | Connection to high-risk port | Medium |
| `brute_force` | Repeated failed access attempts | High |
| `large_packet` | Unusually large packet size | Low |

## 📊 Dashboard URLs

```
Main Dashboard:     http://localhost:5000
API Documentation:  Check this file!
WebSocket:          ws://localhost:5000/socket.io/
```

## 🎨 WebSocket Events

### Client → Server
```javascript
// Connect to server
socket = io();

// Request update
socket.emit('request_update');
```

### Server → Client
```javascript
// Connection established
socket.on('connected', (data) => {
  console.log(data);
});

// New threat detected
socket.on('new_threat', (threat) => {
  console.log('Threat:', threat);
});

// Stats update
socket.on('stats_update', (stats) => {
  console.log('Stats:', stats);
});
```

## 🐛 Troubleshooting

### Common Issues & Solutions

```bash
# Port 5000 already in use
lsof -i :5000
kill -9 <PID>

# Permission denied (network monitoring)
sudo python app.py

# Module not found
pip install -r requirements.txt --force-reinstall

# Virtual environment issues
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Check Application Health

```bash
# Verify server is running
curl http://localhost:5000/api/stats

# Check processes
ps aux | grep python

# View real-time logs
tail -f logs/threat_detector.log

# Check system resources
top -p $(pgrep -f "python app.py")
```

## 📦 Dependencies Quick Install

```bash
# Core dependencies only
pip install Flask flask-socketio psutil scikit-learn pandas numpy

# With production server
pip install gunicorn eventlet

# Complete install
pip install -r requirements.txt
```

## 🚀 Production Checklist

```bash
# 1. Set environment
export FLASK_ENV=production
export SECRET_KEY=$(openssl rand -hex 32)

# 2. Update config
# Edit config.py or set env vars

# 3. Test application
python test_detector.py --test

# 4. Run with Gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app

# 5. Setup process manager (systemd, supervisor, etc.)
sudo systemctl start threat-detector

# 6. Configure reverse proxy (nginx, apache)
# 7. Setup SSL certificate (Let's Encrypt)
# 8. Enable firewall
# 9. Configure monitoring/alerts
# 10. Schedule backups (if using DB)
```

## 📱 Keyboard Shortcuts (Dashboard)

```
F5          Refresh page
Ctrl+R      Reload dashboard
Ctrl+Shift+I  Open developer console
```

## 💡 Pro Tips

```bash
# 1. Run in background
nohup python app.py &

# 2. Run with custom port
export PORT=8080
python app.py

# 3. Increase threat history
export MAX_STORED_THREATS=500

# 4. Faster monitoring
export MONITOR_INTERVAL=1

# 5. Debug mode with auto-reload
export FLASK_DEBUG=True FLASK_ENV=development
python app.py

# 6. Check specific IP reputation
curl "http://localhost:5000/api/scan/8.8.8.8"

# 7. Monitor logs in real-time with grep
tail -f logs/threat_detector.log | grep -i "error\|threat"

# 8. Test with custom thresholds
export PORT_SCAN_THRESHOLD=3
python test_detector.py --port-scan
```

## 📝 File Locations

```
Application:       app.py
Configuration:     config.py
Detection Logic:   threat_detector.py
Tests:            test_detector.py
Dashboard:        templates/dashboard.html
Logs:             logs/threat_detector.log
Environment:      .env
Dependencies:     requirements.txt
```

## 🔗 Useful Links

```
Flask Documentation:     https://flask.palletsprojects.com/
Socket.IO:              https://socket.io/docs/
Scikit-learn:           https://scikit-learn.org/
Chart.js:               https://www.chartjs.org/
psutil:                 https://psutil.readthedocs.io/
```

## 🆘 Getting Help

```bash
# Check logs
cat logs/threat_detector.log

# Verbose mode
export LOG_LEVEL=DEBUG
python app.py

# Test connectivity
curl -I http://localhost:5000

# Check Python version
python3 --version

# Verify installations
pip list | grep -i "flask\|sklearn\|psutil"
```

---

**💡 Tip**: Bookmark this page for quick reference during development and deployment!