#!/bin/bash

# Start Quantum Nexus Web Server

cd ~/quantum-nexus
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the web server
echo "🌐 Starting Web Server on port 5000..."
python web_server.py &

echo "✅ Web Server started!"
echo "📊 Check status: systemctl status quantum-nexus-web"

