#!/bin/bash
# ✅ ВЫПОЛНИТЕ ЭТУ КОМАНДУ НА СЕРВЕРЕ SELECTEL
# Скопируйте всю эту команду и вставьте в терминал сервера

cd /root/quantum-nexus && git pull origin main && chmod +x UPDATE_COMMANDS_FIXED.sh && ./UPDATE_COMMANDS_FIXED.sh

# ИЛИ выполните пошагово:

# Шаг 1: Обновите код
# cd /root/quantum-nexus
# git pull origin main

# Шаг 2: Выполните миграцию базы данных
# sudo -u postgres psql quantum_nexus <<EOF
# ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;
# ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0;
# ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0;
# UPDATE users SET experience = (total_earned * 0.01) + (total_taps * 0.1) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000), level = LEAST(100, FLOOR(SQRT(GREATEST(0, (total_earned * 0.01) + (total_taps * 0.1) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000)) / 100) + 1)), rating = (coins * 0.01) + (total_earned * 0.1) + (total_taps * 0.05) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000000) + (level * 10000) WHERE level IS NULL OR experience IS NULL OR rating IS NULL;
# \q
# EOF

# Шаг 3: Скопируйте файлы
# sudo cp web_app.html /var/www/quantum-nexus/web_app.html

# Шаг 4: Перезапустите сервисы
# sudo systemctl restart quantum-nexus-web.service
# sudo systemctl restart quantum-nexus.service

# Шаг 5: Проверьте статус
# sudo systemctl status quantum-nexus-web.service

