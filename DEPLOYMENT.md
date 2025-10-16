# 🚀 Deployment Guide - Cyber Threat Detector

Complete deployment instructions for various cloud platforms.

## Table of Contents
- [Render.com](#rendercom)
- [Railway.app](#railwayapp)
- [Heroku](#heroku)
- [AWS EC2](#aws-ec2)
- [DigitalOcean](#digitalocean)
- [Docker](#docker)
- [Local Development](#local-development)

---

## Render.com

### Quick Deploy

1. **Create `render.yaml`** in project root:

```yaml
services:
  - type: web
    name: cyber-threat-detector
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: PORT_SCAN_THRESHOLD
        value: 10
      - key: MONITOR_INTERVAL
        value: 2
```

2. **Deploy via GitHub**:
   - Push code to GitHub
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-deploy using `render.yaml`

3. **Deploy via CLI**:

```bash
# Install Render CLI
npm install -g @render/cli

# Login
render login

# Deploy
render blueprint launch
```

### Important Notes
- Free tier may have cold starts
- Network monitoring features may be limited in containers
- Use for demonstration purposes

---

## Railway.app

### Quick Deploy

1. **Install Railway CLI**:

```bash
npm install -g @railway/cli
```

2. **Initialize and Deploy**:

```bash
# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=$(openssl rand -hex 32)

# Deploy
railway up
```

3. **Using `railway.json`**:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

4. **Via GitHub**:
   - Connect GitHub repository in Railway dashboard
   - Railway auto-detects Python and deploys
   - Set environment variables in dashboard

### Configuration

```bash
# Set variables
railway variables set PORT_SCAN_THRESHOLD=10
railway variables set DDOS_PACKET_THRESHOLD=1000
railway variables set MONITOR_INTERVAL=2

# View logs
railway logs

# Open deployed app
railway open
```

---

## Heroku

### Prerequisites

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# OR
curl https://cli-assets.heroku.com/install.sh | sh  # Linux
```

### Deploy Steps

1. **Create `Procfile`**:

```
web: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
```

2. **Create `runtime.txt`**:

```
python-3.9.18
```

3. **Deploy**:

```bash
# Login
heroku login

# Create app
heroku create your-threat-detector

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set PORT_SCAN_THRESHOLD=10

# Deploy
git push heroku main

# Scale dyno
heroku ps:scale web=1

# View logs
heroku logs --tail

# Open app
heroku open
```

### Heroku-specific Notes

- Free tier sleeps after 30 minutes of inactivity
- Network monitoring limited in container environment
- Consider upgrading to Hobby tier for production

---

## AWS EC2

### Launch Instance

1. **Create EC2 Instance**:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (free tier) or t2.small
   - Security Group: Open ports 22 (SSH), 80 (HTTP), 443 (HTTPS), 5000

2. **Connect via SSH**:

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install -y python3-pip python3-venv nginx nmap

# Install certbot for HTTPS
sudo apt install -y certbot python3-certbot-nginx
```

4. **Deploy Application**:

```bash
# Clone repository
git clone https://github.com/yourusername/cyber-threat-detector.git
cd cyber-threat-detector

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=$(openssl rand -hex 32)

# Test application
python app.py
```

5. **Setup Systemd Service**:

Create `/etc/systemd/system/threat-detector.service`:

```ini
[Unit]
Description=Cyber Threat Detector
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/cyber-threat-detector
Environment="PATH=/home/ubuntu/cyber-threat-detector/venv/bin"
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=your-secret-key"
ExecStart=/home/ubuntu/cyber-threat-detector/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable threat-detector
sudo systemctl start threat-detector
sudo systemctl status threat-detector
```

6. **Configure Nginx**:

Create `/etc/nginx/sites-available/threat-detector`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/threat-detector /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Setup HTTPS** (Optional):

```bash
sudo certbot --nginx -d your-domain.com
```

---

## DigitalOcean

### Using Droplet

1. **Create Droplet**:
   - Choose Ubuntu 22.04
   - Select plan (Basic $6/month recommended)
   - Add SSH key

2. **Follow AWS EC2 steps above** (same process)

### Using App Platform

1. **Connect GitHub**:
   - Go to DigitalOcean App Platform
   - Connect GitHub repository
   - Auto-detect Python

2. **Configure Build**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --worker-class eventlet -w 1 app:app`

3. **Set Environment Variables**:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
PORT_SCAN_THRESHOLD=10
```

4. **Deploy**: DigitalOcean handles the rest!

---

## Docker

### Single Container

1. **Build Image**:

```bash
docker build -t threat-detector .
```

2. **Run Container**:

```bash
docker run -d \
  --name threat-detector \
  --network host \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -p 5000:5000 \
  threat-detector
```

3. **View Logs**:

```bash
docker logs -f threat-detector
```

### Docker Compose

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

### Push to Registry

```bash
# Tag image
docker tag threat-detector yourusername/threat-detector:latest

# Login
docker login

# Push
docker push yourusername/threat-detector:latest
```

---

## Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/cyber-threat-detector.git
cd cyber-threat-detector

# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate
# OR Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment
export FLASK_ENV=development
export SECRET_KEY=dev-secret-key

# Run application
python app.py
```

### Run with Admin Privileges

```bash
# Linux/Mac
sudo -E venv/bin/python app.py

# Windows (Run as Administrator)
python app.py
```

### Development with Auto-Reload

```bash
export FLASK_DEBUG=True
python app.py
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FLASK_ENV` | Yes | development | Environment mode |
| `SECRET_KEY` | Yes | - | Secret key for sessions |
| `PORT_SCAN_THRESHOLD` | No | 10 | Ports for scan detection |
| `DDOS_PACKET_THRESHOLD` | No | 1000 | Packets/sec threshold |
| `BRUTE_FORCE_THRESHOLD` | No | 5 | Failed attempts threshold |
| `MONITOR_INTERVAL` | No | 2 | Seconds between scans |
| `MAX_STORED_THREATS` | No | 100 | Max threats in memory |
| `LOG_LEVEL` | No | INFO | Logging level |

---

## Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Configure HTTPS/SSL
- [ ] Setup firewall rules
- [ ] Enable monitoring/logging
- [ ] Configure backup strategy
- [ ] Set up alerting (email/webhook)
- [ ] Test all detection features
- [ ] Document any customizations
- [ ] Setup automated restarts
- [ ] Configure rate limiting
- [ ] Review security settings

---

## Troubleshooting

### Common Issues

**Port Already in Use**:
```bash
# Find process
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Permission Denied**:
```bash
# Run with sudo
sudo -E python app.py
```

**Module Not Found**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**WebSocket Connection Failed**:
- Check firewall allows WebSocket connections
- Ensure nginx/proxy configured for WebSocket upgrades
- Verify port 5000 is accessible

---

## Support

For deployment issues:
- Check application logs
- Review platform-specific documentation
- Ensure all prerequisites are met
- Verify environment variables are set

Happy Deploying! 🚀