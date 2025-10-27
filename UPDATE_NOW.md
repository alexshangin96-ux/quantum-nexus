# ОБНОВИТЕ БОТА НА СЕРВЕРЕ

## Команды для выполнения:

```bash
cd /root/quantum-nexus
git pull origin main

# Найти процесс бота
ps aux | grep "bot.py" | grep -v grep

# Убить процесс бота
pkill -f "bot.py"

# Запустить бота заново
cd /root/quantum-nexus
source venv/bin/activate
nohup python bot.py > bot.log 2>&1 &

# Проверить что бот запустился
tail -f bot.log
```

## Или используйте:

```bash
./RESTART_BOT.sh
```

## Что изменилось:
✅ Убрано лишнее сообщение "invoice отправлен"
✅ Добавлены товары 3, 4, 5 (Бонусный, VIP, Легендарный)
✅ Товары настроены в handlers.py с правильными ценами

После обновления все 5 товаров должны работать.
