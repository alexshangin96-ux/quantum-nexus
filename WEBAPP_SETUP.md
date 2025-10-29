# Настройка Web App для Quantum Nexus

## Установка зависимостей

На сервере выполните:

```bash
cd ~/quantum-nexus
source venv/bin/activate
pip install Flask flask-cors
```

## Настройка Nginx для Web App

```bash
sudo nano /etc/nginx/sites-available/quantum-nexus
```

Измените конфигурацию:

```nginx
server {
    listen 80;
    server_name quantum-nexus.ru;

    # Serve static files
    location /web_app.html {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo systemctl restart nginx
```

## Создание systemd сервиса для Web Server

```bash
sudo nano /etc/systemd/system/quantum-nexus-web.service
```

Содержимое:

```ini
[Unit]
Description=Quantum Nexus Web Server
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/quantum-nexus
Environment="PATH=/root/quantum-nexus/venv/bin"
ExecStart=/root/quantum-nexus/venv/bin/python web_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start quantum-nexus-web
sudo systemctl enable quantum-nexus-web
sudo systemctl status quantum-nexus-web
```

## Проверка работы

1. Проверьте, что Web Server запущен: `sudo systemctl status quantum-nexus-web`
2. Откройте браузер: `http://quantum-nexus.ru/web_app.html`
3. В Telegram откройте бота и нажмите кнопку "🎮 Открыть игру"

Готово! Ваш Web App работает внутри Telegram!



