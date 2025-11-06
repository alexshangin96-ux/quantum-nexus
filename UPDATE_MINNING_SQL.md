# 🚀 SQL Миграция для майнинга v6.0

## 📋 Команды для обновления базы данных на Selectel

### 1. Подключение к серверу
```bash
ssh root@your-server-ip
```

### 2. Обновление кода с GitHub
```bash
cd /root/quantum-nexus
git pull origin main
```

### 3. Выполнение SQL миграции
```bash
cd /root/quantum-nexus
cat ADD_MINING_LEVELS.sql
```

### 4. Подключение к PostgreSQL и выполнение миграции

**Вариант 1: Через psql (если у вас PostgreSQL)**
```bash
sudo -u postgres psql quantum_nexus_db < ADD_MINING_LEVELS.sql
```

**Вариант 2: Через psql вручную**
```bash
sudo -u postgres psql quantum_nexus_db
```

Затем введите SQL команды:
```sql
-- Add mining_coins_levels column
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS mining_coins_levels TEXT DEFAULT '{}';

-- Add mining_quanhash_levels column
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS mining_quanhash_levels TEXT DEFAULT '{}';

-- Add mining_vip_levels column
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS mining_vip_levels TEXT DEFAULT '{}';

-- Initialize existing users with empty JSON objects
UPDATE users 
SET mining_coins_levels = '{}' 
WHERE mining_coins_levels IS NULL;

UPDATE users 
SET mining_quanhash_levels = '{}' 
WHERE mining_quanhash_levels IS NULL;

UPDATE users 
SET mining_vip_levels = '{}' 
WHERE mining_vip_levels IS NULL;

-- Verify
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' 
AND column_name LIKE 'mining_%_levels'
ORDER BY column_name;

\q
```

**Вариант 3: Через Python скрипт (если не работает psql)**
```bash
cd /root/quantum-nexus
python3 migration_add_mining_levels.py
```

### 5. Копирование файлов
```bash
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo cp web_server.py /var/www/quantum-nexus/web_server.py
sudo cp models.py /var/www/quantum-nexus/models.py
```

### 6. Перезапуск сервисов
```bash
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service
```

### 7. Проверка
```bash
sudo systemctl status quantum-nexus-web.service
sudo journalctl -u quantum-nexus-web.service -f
```

## 🚀 Быстрый способ (копируйте все)

```bash
cd /root/quantum-nexus
git pull origin main

# Выполнить SQL миграцию
sudo -u postgres psql quantum_nexus_db < ADD_MINING_LEVELS.sql

# Или если не работает PostgreSQL
python3 migration_add_mining_levels.py

# Скопировать файлы
sudo cp web_app.html web_server.py models.py /var/www/quantum-nexus/

# Перезапустить
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service
```

## 🆘 Если возникли ошибки

### Ошибка "column already exists"
Это нормально! Значит поля уже добавлены. Продолжайте дальше.

### Ошибка "database does not exist"
Найдите правильное имя базы:
```bash
sudo -u postgres psql -l
```

### Ошибка "permission denied"
Попробуйте:
```bash
sudo -u postgres psql -d quantum_nexus_db
```

### Не знаете имя базы данных
Проверьте в конфиге:
```bash
cat quantum-nexus/database.py | grep database
```

## ✅ Проверка успешности миграции

```bash
sudo -u postgres psql quantum_nexus_db -c "SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name LIKE 'mining_%_levels';"
```

Должны увидеть 3 колонки:
- mining_coins_levels
- mining_quanhash_levels
- mining_vip_levels





