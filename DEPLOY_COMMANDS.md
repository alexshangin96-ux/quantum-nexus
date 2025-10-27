# Команды для обновления Quantum Nexus на сервере

## Быстрое обновление (один раз выполнить на сервере)

### Вариант 1: Через SSH + команды
```bash
ssh root@ваш_IP
cd /root/quantum-nexus
git pull origin main
cp admin.html /var/www/quantum-nexus/
systemctl restart quantum-nexus-web
systemctl status quantum-nexus-web
```

### Вариант 2: Использовать готовый скрипт
```bash
ssh root@ваш_IP
cd /root/quantum-nexus
chmod +x UPDATE_SERVER.sh
./UPDATE_SERVER.sh
```

## Полное обновление (если нужно пересобрать всё)

```bash
ssh root@ваш_IP

# Перейти в директорию проекта
cd /root/quantum-nexus

# Получить последние изменения
git pull origin main

# Обновить Python зависимости
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Скопировать файлы
cp admin.html /var/www/quantum-nexus/
cp web_app.html /var/www/quantum-nexus/

# Перезапустить сервисы
systemctl restart quantum-nexus-bot
systemctl restart quantum-nexus-web

# Проверить статус
systemctl status quantum-nexus-bot
systemctl status quantum-nexus-web
```

## Если нужно обновить базу данных

```bash
ssh root@ваш_IP
cd /root/quantum-nexus
source venv/bin/activate
python -c "from database import init_db; init_db()"
```

## Проверка работы

После обновления проверьте:
- Админ-панель: https://quantum-nexus.ru/admin
- Бот отвечает на команды в Telegram
- Веб-приложение открывается корректно

## Логи для отладки

```bash
# Логи бота
journalctl -u quantum-nexus-bot -f

# Логи веб-сервера
journalctl -u quantum-nexus-web -f

# Логи Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

