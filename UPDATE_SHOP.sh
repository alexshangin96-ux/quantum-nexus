#!/bin/bash
# Full update for new shop system

echo "🛒 Обновление магазина..."

cd ~/quantum-nexus

# Update code
git pull origin main

# Copy updated files
sudo cp web_server.py /root/quantum-nexus/web_server.py
sudo cp web_app.html /var/www/quantum-nexus/web_app.html

# Set permissions
sudo chmod 644 /root/quantum-nexus/web_server.py
sudo chmod 644 /var/www/quantum-nexus/web_app.html

# Restart services
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service

echo "✅ Магазин обновлен!"







