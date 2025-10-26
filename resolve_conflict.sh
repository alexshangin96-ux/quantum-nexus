#!/bin/bash
# Force resolve merge conflict and update admin panel

cd /root/quantum-nexus

# Discard all local changes
git reset --hard HEAD
git clean -fd

# Pull latest changes
git pull origin main

# Restart web server
sudo systemctl restart quantum-nexus-web

echo "✅ Conflict resolved! Admin panel updated!"
