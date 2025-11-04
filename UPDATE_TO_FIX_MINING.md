# Исправление ошибки покупки майнинг-машин

## Проблема
Ошибка "invalid literal" или "invalid machine id" при покупке майнинг-машин.

## Решение

### Вариант 1: Обновление до последней версии (рекомендуется)

```bash
cd /root/quantum-nexus

# Разрешить конфликт если есть
git merge --abort 2>/dev/null
git reset --hard HEAD

# Получить последние изменения
git fetch origin
git pull origin main

# Скопировать файлы
sudo cp web_server.py /root/quantum-nexus/web_server.py

# Перезапустить сервис
sudo systemctl restart quantum-nexus-web.service
```

### Вариант 2: Ручное исправление (если git pull не работает)

Если на сервере версия 8d8ebf3 (v6.7.58), нужно добавить обработку ошибок в функцию `buy_machine`.

Найдите в `web_server.py` функцию `buy_machine()` и найдите строки:

```python
if currency == 'coins':
    levels = json.loads(user.mining_coins_levels or '{}')
    current_level = levels.get(machine_id, 0)
elif currency == 'quanhash':
    levels = json.loads(user.mining_quanhash_levels or '{}')
    current_level = levels.get(machine_id, 0)
```

Замените на:

```python
if currency == 'coins':
    try:
        levels = json.loads(user.mining_coins_levels or '{}')
    except (json.JSONDecodeError, TypeError, ValueError):
        levels = {}
    current_level = levels.get(machine_id, 0)
elif currency == 'quanhash':
    try:
        levels = json.loads(user.mining_quanhash_levels or '{}')
    except (json.JSONDecodeError, TypeError, ValueError):
        levels = {}
    current_level = levels.get(machine_id, 0)
```

Также найдите место обновления levels (после покупки):

```python
if currency == 'coins':
    levels = json.loads(user.mining_coins_levels or '{}')
    levels[machine_id] = new_level
    user.mining_coins_levels = json.dumps(levels)
elif currency == 'quanhash':
    levels = json.loads(user.mining_quanhash_levels or '{}')
    levels[machine_id] = new_level
    user.mining_quanhash_levels = json.dumps(levels)
```

Замените на:

```python
try:
    if currency == 'coins':
        try:
            levels = json.loads(user.mining_coins_levels or '{}')
        except (json.JSONDecodeError, TypeError, ValueError):
            levels = {}
        levels[machine_id] = new_level
        user.mining_coins_levels = json.dumps(levels)
    elif currency == 'quanhash':
        try:
            levels = json.loads(user.mining_quanhash_levels or '{}')
        except (json.JSONDecodeError, TypeError, ValueError):
            levels = {}
        levels[machine_id] = new_level
        user.mining_quanhash_levels = json.dumps(levels)
except Exception as e:
    print(f"Error updating levels JSON: {e}")
```

После исправления:

```bash
sudo cp web_server.py /root/quantum-nexus/web_server.py
sudo systemctl restart quantum-nexus-web.service
```

## Проверка

После обновления проверьте логи:

```bash
journalctl -u quantum-nexus-web.service -f
```

Попробуйте купить майнинг-машину - ошибки не должно быть.
