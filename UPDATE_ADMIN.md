# Обновление админ-панели на сервере

## 1. Подключитесь к серверу
```bash
ssh root@quantum-nexus.ru
```

## 2. Перейдите в директорию проекта
```bash
cd /root/quantum-nexus
```

## 3. Обновите код с GitHub
```bash
git pull origin main
```

## 4. Проверьте конфигурацию Nginx
```bash
cat /etc/nginx/sites-available/quantum-nexus
```

Убедитесь, что есть роут для админ-панели:
```nginx
location /admin {
    alias /var/www/quantum-nexus/admin.html;
}
```

Если его нет, добавьте его.

## 5. Скопируйте файл
```bash
cp admin.html /var/www/quantum-nexus/
```

## 6. Перезапустите веб-сервер
```bash
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx
```

## 7. Проверьте статус
```bash
sudo systemctl status quantum-nexus-web
sudo systemctl status nginx
```

## 8. Откройте админ-панель
В браузере перейдите на:
```
https://quantum-nexus.ru/admin
```

## Если не работает, проверьте логи
```bash
sudo journalctl -u quantum-nexus-web -f
sudo tail -f /var/log/nginx/error.log
```

