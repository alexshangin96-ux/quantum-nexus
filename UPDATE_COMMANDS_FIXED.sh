#!/bin/bash
# Complete update script for sounds and leaderboard system
# Execute this on Selectel server

set -e  # Exit on error

echo "🚀 Starting Quantum Nexus update..."

# Navigate to project directory
cd /root/quantum-nexus || exit 1

echo "📥 Pulling latest code from GitHub..."
git pull origin main

echo "🗄️ Adding new columns to database..."
# Use psql to execute SQL migration
sudo -u postgres psql quantum_nexus <<EOF
ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0;
UPDATE users 
SET experience = (total_earned * 0.01) + (total_taps * 0.1) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000),
    level = LEAST(100, FLOOR(SQRT(GREATEST(0, (total_earned * 0.01) + (total_taps * 0.1) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000)) / 100) + 1)),
    rating = (coins * 0.01) + (total_earned * 0.1) + (total_taps * 0.05) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000000) + (level * 10000)
WHERE level IS NULL OR experience IS NULL OR rating IS NULL;
SELECT COUNT(*) as total_users, AVG(level) as avg_level, MAX(level) as max_level, AVG(rating) as avg_rating, MAX(rating) as max_rating FROM users;
\q
EOF

echo "📁 Copying updated files..."
sudo cp web_app.html /var/www/quantum-nexus/web_app.html

echo "🔄 Restarting services..."
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service

echo "✅ Checking service status..."
sudo systemctl status quantum-nexus-web.service --no-pager
sudo systemctl status quantum-nexus.service --no-pager

echo "🎉 Update completed successfully!"

