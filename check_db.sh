#!/bin/bash
echo "=== Checking PostgreSQL status ==="
sudo systemctl status postgresql

echo ""
echo "=== Checking connection ==="
sudo -u postgres psql -c "\l" | grep quantum

echo ""
echo "=== Checking tables ==="
sudo -u postgres psql -d quantum -c "\dt"

echo ""
echo "=== Fixing database if needed ==="
cd ~/quantum-nexus
python3 -c "from database import Base, engine; Base.metadata.create_all(engine)"

echo ""
echo "Done!"

