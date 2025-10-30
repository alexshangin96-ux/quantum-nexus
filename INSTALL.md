# Инструкция по установке Quantum Nexus на Selectel

## Быстрая установка

```bash
# 1. Обновление системы
sudo apt update && sudo apt upgrade -y

# 2. Установка необходимых пакетов
sudo apt install -y python3 python3-pip python3-venv git postgresql postgresql-contrib redis-server nginx

# 3. Настройка PostgreSQL
sudo -u postgres psql <<EOF
CREATE USER quantum WITH PASSWORD 'ChangeMe123!';
CREATE DATABASE quantum_nexus OWNER quantum;
GRANT ALL PRIVILEGES ON DATABASE quantum_nexus TO quantum;
\q
EOF

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
cp config.py config.py.backup
nano config.py  # Отредактируйте DATABASE_URL

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
User=$USER
WorkingDirectory=/home/$USER/quantum-nexus
Environment="PATH=/home/$USER/quantum-nexus/venv/bin"
ExecStart=/home/$USER/quantum-nexus/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 10. Запуск сервиса
sudo systemctl daemon-reload
sudo systemctl start quantum-nexus
sudo systemctl enable quantum-nexus

# 11. Проверка статуса
sudo systemctl status quantum-nexus
journalctl -u quantum-nexus -f
```

## Настройка Nginx

```bash
sudo nano /etc/nginx/sites-available/quantum-nexus
```

Содержимое:

```nginx
server {
    listen 80;
    server_name quantum-nexus.ru;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name quantum-nexus.ru;

    ssl_certificate /etc/letsencrypt/live/quantum-nexus.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/quantum-nexus.ru/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/quantum-nexus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# SSL сертификат
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d quantum-nexus.ru
```

## Обновление приложения

```bash
cd ~/quantum-nexus
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart quantum-nexus
```

## Мониторинг

```bash
# Логи
journalctl -u quantum-nexus -f

# Статус
systemctl status quantum-nexus

# Перезапуск
sudo systemctl restart quantum-nexus
```

## Структура файлов

- `bot.py` - главный файл бота
- `config.py` - конфигурация
- `database.py` - работа с БД
- `models.py` - модели данных
- `handlers.py` - обработчики команд
- `keyboards.py` - клавиатуры
- `utils.py` - утилиты
