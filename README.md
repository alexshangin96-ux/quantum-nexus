# Quantum Nexus - Игра Tap-to-Earn для Telegram

## Описание
Quantum Nexus - это инновационная игра для Telegram с механикой заработка коинов и QuanHash через тапы, майнинг и стратегическое развитие.

## Основные возможности

- 🎮 **Тапалка** - зарабатывай коины тапами
- 💰 **Двойная валюта** - коины и QuanHash
- ⚡ **Энергия** - ограничивает активность
- 🛒 **Магазин бустов** - усиление доходов
- 🏭 **Криптомашины** - майнинг QuanHash
- 💳 **Карточки** - пассивный доход
- 🏆 **Рейтинги** - топ игроков
- 👥 **Реферальная система**
- ⏰ **Оффлайн доход** - до 3 часов
- 🛡️ **Защита от автокликера**

## Установка на Selectel

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install -y python3 python3-pip python3-venv git

# Установка PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Настройка PostgreSQL
sudo -u postgres psql -c "CREATE USER quantum WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "CREATE DATABASE quantum_nexus OWNER quantum;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE quantum_nexus TO quantum;"
```

### 2. Клонирование репозитория

```bash
cd ~
git clone https://github.com/alexshangin96-ux/quantum-nexus.git
cd quantum-nexus
```

### 3. Настройка окружения

```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 4. Настройка конфигурации

```bash
# Копирование файла конфигурации
cp config.py.example config.py

# Редактирование config.py
nano config.py
```

В файле `config.py` укажите:
- Ваш Telegram Bot Token
- URL приложения
- Настройки базы данных

### 5. Инициализация базы данных

```bash
# Запуск миграций
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# Создание начальных данных
python init_db.py
```

### 6. Настройка systemd сервиса

```bash
sudo nano /etc/systemd/system/quantum-nexus.service
```

Добавьте следующее содержимое:

```ini
[Unit]
Description=Quantum Nexus Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/quantum-nexus
Environment="PATH=/home/your_username/quantum-nexus/venv/bin"
ExecStart=/home/your_username/quantum-nexus/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 7. Запуск сервиса

```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Запуск сервиса
sudo systemctl start quantum-nexus

# Автозапуск при загрузке
sudo systemctl enable quantum-nexus

# Проверка статуса
sudo systemctl status quantum-nexus
```

### 8. Настройка Nginx (опционально)

```bash
sudo apt install -y nginx
sudo nano /etc/nginx/sites-available/quantum-nexus
```

```nginx
server {
    listen 80;
    server_name quantum-nexus.ru;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/quantum-nexus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Настройка SSL (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d quantum-nexus.ru
```

## Мониторинг и логи

```bash
# Просмотр логов
sudo journalctl -u quantum-nexus -f

# Статус сервиса
sudo systemctl status quantum-nexus

# Рестарт сервиса
sudo systemctl restart quantum-nexus
```

## Обновление приложения

```bash
cd ~/quantum-nexus
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart quantum-nexus
```

## Структура проекта

```
quantum-nexus/
├── bot.py                 # Главный файл бота
├── database.py            # Работа с БД
├── models.py              # Модели данных
├── handlers/              # Обработчики команд
├── keyboards/             # Клавиатуры
├── utils/                 # Утилиты
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости
└── README.md             # Документация
```

## Разработка

Для локальной разработки:

```bash
python bot.py
```

## Лицензия

MIT License
