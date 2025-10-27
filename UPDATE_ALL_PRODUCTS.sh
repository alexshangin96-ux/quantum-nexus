#!/bin/bash

cd /root/quantum-nexus

git pull origin main
systemctl restart quantum-nexus-web.service

echo "✅ Обновление завершено"
echo "Теперь откройте /start в боте"

