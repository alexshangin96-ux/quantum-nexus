# Инструкция по установке Quantum Nexus на Selectel

## Быстрая установка

```bash
# 1. Обновление системы
sudo apt update && sudo apt upgrade -y

# 2. Установка необходимых пакетов
sudo apt install -y python3 python3-pip python3-venv git postgresql postgresql-contrib redis-server nginx

# 3. Настройка PostgreSQL
# Создание пользователя с паролем
sudo -u postgres psql -c "CREATE USER quantum WITH PASSWORD 'quantum123';"
sudo -u postgres psql -c "ALTER USER quantum CREATEDB;"
sudo -u postgres createdb -O quantum quantum_nexus

# Установка Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 4. Клонирование репозитория
cd ~
git clone https://github.com/alexshangin96-ux/quantum-nexus.git
cd quantum-nexus

# 5. Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# 6. Установка зависимостей
pip install -r requirements.txt

# 7. Настройка конфигурации
# ОТРЕДАКТИРУЙТЕ config.py - измените пароль БД на 'quantum123'
nano config.py

# Измените строку:
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://quantum:quantum123@localhost:5432/quantum_nexus")

# 8. Инициализация базы данных
python -c "from database import init_db; init_db()"

# 9. Создание systemd сервиса
sudo nano /etc/systemd/system/quantum-nexus.service
```

Содержимое файла `/etc/systemd/system/quantum-nexus.service`:

```ini
[Unit]
Description=Quantum Nexus Telegram Bot
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/quantum-nexus
Environment="PATH=/root/quantum-nexus/venv/bin"
ExecStart=/root/quantum-nexus/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**ВАЖНО:** Замените `User=root` и пути `/root/quantum-nexus` на ваши реальные значения.

```bash
# 10. Запуск сервиса
sudo systemctl daemon-reload
sudo systemctl start quantum-nexus
sudo systemctl enable quantum-nexus

# 11. Проверка статуса
sudo systemctl status quantum-nexus
journalctl -u quantum-nexus -f
```
