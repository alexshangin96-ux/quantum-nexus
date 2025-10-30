# Quantum Nexus - Deployment Guide

## Quick Start

### 1. Install Dependencies

```bash
cd ~/quantum-nexus
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Database

Update `config.py` with your PostgreSQL password:
```python
DATABASE_URL = "postgresql://quantum:quantum123@localhost:5432/quantum_nexus"
```

### 3. Start Bot

```bash
sudo systemctl start quantum-nexus
sudo systemctl enable quantum-nexus
```

### 4. Setup HTTPS and Web Server

```bash
chmod +x setup-https.sh start-web-server.sh
./setup-https.sh
./start-web-server.sh
```

Or manually:

```bash
# Setup HTTPS
sudo certbot certonly --standalone -d quantum-nexus.ru

# Configure Nginx (see WEBAPP_SETUP.md)

# Start Web Server
sudo systemctl start quantum-nexus-web
sudo systemctl enable quantum-nexus-web
```

### 5. Check Status

```bash
# Check Bot
sudo systemctl status quantum-nexus

# Check Web Server
sudo systemctl status quantum-nexus-web

# Check Nginx
sudo systemctl status nginx
```

## Troubleshooting

### 502 Bad Gateway

**Problem:** Web server not running or not accessible

**Solution:**
```bash
# Check if web server is running
sudo systemctl status quantum-nexus-web

# Start web server
sudo systemctl start quantum-nexus-web

# Check logs
journalctl -u quantum-nexus-web -f
```

### SSL Certificate Issues

**Problem:** HTTPS not working

**Solution:**
```bash
# Renew certificate
sudo certbot renew

# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Port Already in Use

**Problem:** Port 5000 is already in use

**Solution:**
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill the process or change port in web_server.py
```

## Production Deployment

### Using systemd for Web Server

Create `/etc/systemd/system/quantum-nexus-web.service`:

```ini
[Unit]
Description=Quantum Nexus Web Server
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/quantum-nexus
Environment="PATH=/root/quantum-nexus/venv/bin"
ExecStart=/root/quantum-nexus/venv/bin/python web_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start quantum-nexus-web
sudo systemctl enable quantum-nexus-web
```

### Auto-renew SSL Certificates

```bash
# Add to crontab
sudo crontab -e

# Add this line:
0 0 * * * certbot renew --quiet
```

## Testing

1. **Test Bot:** Send `/start` to `@qanexus_bot`
2. **Test Web App:** Open `https://quantum-nexus.ru/web_app.html`
3. **Test API:**
```bash
curl -X POST https://quantum-nexus.ru/api/user_data \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789}'
```






