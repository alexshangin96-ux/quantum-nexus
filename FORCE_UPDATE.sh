#!/bin/bash
# Force update admin panel

cd /root/quantum-nexus

# Force pull
git fetch origin
git reset --hard origin/main
git clean -fd -x

# Verify file
echo "=== Checking admin.html ==="
if [ -f "admin.html" ]; then
    echo "✅ admin.html exists"
    echo "File size: $(du -h admin.html | cut -f1)"
    echo "File lines: $(wc -l < admin.html)"
else
    echo "❌ admin.html NOT FOUND!"
fi

# Restart services
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx

echo ""
echo "✅ Force update complete!"
echo "Visit: https://quantum-nexus.ru/admin"
