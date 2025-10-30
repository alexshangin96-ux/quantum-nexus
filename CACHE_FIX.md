# Исправление кеша - Почему изменения не применяются

## Проблема
Файлы обновлены на сервере, но в приложении ничего не изменилось.

## Решение

Выполните на сервере:

```bash
cd /root/quantum-nexus

# 1. Получить последние изменения
git pull origin main

# 2. Скопировать web_app.html в правильное место
sudo cp web_app.html /var/www/quantum-nexus/
sudo chown www-data:www-data /var/www/quantum-nexus/web_app.html

# 3. Очистить кеш Nginx
sudo systemctl reload nginx

# 4. Перезапустить Flask сервер
sudo systemctl restart quantum-nexus-web

# 5. Проверить что файл обновился
ls -lh /var/www/quantum-nexus/web_app.html
head -n 10 /var/www/quantum-nexus/web_app.html
```

## Проверка

Откройте файл напрямую в браузере:
```
https://quantum-nexus.ru/web_app.html?v=2.0
```

Проверьте заголовок - должно быть "Quantum Nexus" без иконок ⚛️.

## Если всё равно не работает

Добавьте в начало `web_app.html` комментарий с версией:

```html
<!-- Quantum Nexus v2.0 - Updated -->
```

Или измените что-то визуально очевидное, чтобы убедиться что файл обновился.






