# Проверка обновления магазина

## Команды для выполнения на сервере:

```bash
# 1. Перейти в директорию проекта
cd /root/quantum-nexus

# 2. Получить последние изменения
git pull origin main

# 3. Проверить что файл обновился
head -n 10 web_app.html | grep "Quantum Nexus"

# 4. Перезапустить web сервер
systemctl restart quantum-nexus-web.service

# 5. Проверить статус
systemctl status quantum-nexus-web.service

# 6. Посмотреть логи
journalctl -u quantum-nexus-web.service -n 50
```

## Если изменения не видны в Telegram:

### Очистить кэш Telegram Mini App:
1. Удалите приложение из Telegram
2. Добавьте бота снова
3. Откройте игру

### Или добавьте версию к URL:
В `handlers.py` измените:
```python
WebAppInfo(url="https://quantum-nexus.ru/web_app.html?v=3.0")
```

## Проверка что изменения применены:

Откройте в браузере:
```
https://quantum-nexus.ru/web_app.html
```

Нажмите Ctrl+F и найдите:
- "VIP стартовый" - должно быть новое описание
- "💎 VIP стартовый" - должно быть с иконкой 32px

Если видите старое - кеш не обновился.







