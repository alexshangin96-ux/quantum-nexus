#!/bin/bash

# Quantum Nexus HTTPS Setup Script

echo "🔒 Setting up HTTPS for quantum-nexus.ru..."

# Install Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx -y

# Stop Nginx temporarily
sudo systemctl stop nginx

# Get SSL certificate
sudo certbot certonly --standalone -d quantum-nexus.ru --email admin@quantum-nexus.ru --agree-tos --non-interactive

# Create Nginx config with SSL
sudo tee /etc/nginx/sites-available/quantum-nexus > /dev/null <<EOF
server {
    listen 80;
    server_name quantum-nexus.ru;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name quantum-nexus.ru;

    ssl_certificate /etc/letsencrypt/live/quantum-nexus.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/quantum-nexus.ru/privkey.pem;

    # Serve Web App
    location /web_app.html {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/quantum-nexus /etc/nginx/sites-enabled/

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx

echo "✅ HTTPS setup complete!"
echo "🌐 Your site is now available at: https://quantum-nexus.ru"






