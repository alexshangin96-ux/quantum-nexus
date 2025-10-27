#!/bin/bash
# Fix merge conflict and update admin panel

cd /root/quantum-nexus

# Save local changes or discard them
git stash

# Pull latest changes
git pull origin main

# Check if file exists
if [ -f "admin.html" ]; then
    echo "✅ admin.html exists"
else
    echo "❌ admin.html not found!"
fi

# Restart web server
sudo systemctl restart quantum-nexus-web

echo "✅ Admin panel updated!"

