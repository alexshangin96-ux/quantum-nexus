#!/bin/bash

echo "=== Автоматическая генерация 137 ботов ==="

cd /root/quantum-nexus

# Activate virtual environment
source venv/bin/activate

# Run the generation script
python3 generate_bot_users.py

# Restart web server to apply changes
systemctl restart quantum-nexus-web

echo "=== Готово! ==="





