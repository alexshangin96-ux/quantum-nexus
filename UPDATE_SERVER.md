# Обновление сервера

## 1. Скачать последние изменения

```bash
cd ~/quantum-nexus
git pull origin main
```

## 2. Установить зависимости

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Запустить Web Server

Создайте сервис для Web Server:

```bash
sudo nano /etc/systemd/system/quantum-nexus-web.service
```

Скопируйте:

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
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запустите:

```bash
sudo systemctl daemon-reload
sudo systemctl start quantum-nexus-web
sudo systemctl enable quantum-nexus-web
sudo systemctl status quantum-nexus-web
```

## 4. Настроить HTTPS

```bash
# Установите Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получите SSL сертификат
sudo certbot certonly --standalone -d quantum-nexus.ru

# Настройте Nginx
sudo nano /etc/nginx/sites-available/quantum-nexus
```

Скопируйте в файл:

```nginx
server {
    listen 80;
    server_name quantum-nexus.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name quantum-nexus.ru;

    ssl_certificate /etc/letsencrypt/live/quantum-nexus.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/quantum-nexus.ru/privkey.pem;

    location /web_app.html {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Включите сайт
sudo ln -sf /etc/nginx/sites-available/quantum-nexus /etc/nginx/sites-enabled/

# Проверьте и перезапустите
sudo nginx -t
sudo systemctl restart nginx
```

## 5. Проверка

```bash
# Проверьте статус Web Server
sudo systemctl status quantum-nexus-web

# Проверьте логи
journalctl -u quantum-nexus-web -f
```

Готово! Откройте `https://quantum-nexus.ru/web_app.html`

