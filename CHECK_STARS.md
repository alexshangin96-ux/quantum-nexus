# Проверка работает ли Stars оплата

## Шаг 1: Обновите бота на сервере

```bash
ssh root@ваш_IP
cd /root/quantum-nexus
git pull origin main
systemctl restart quantum-nexus-bot
```

## Шаг 2: Проверьте логи

```bash
journalctl -u quantum-nexus-bot -f
```

## Шаг 3: Протестируйте покупку

1. Откройте бота @qanexus_bot в Telegram
2. Отправьте: `/start buy_stars_1`
3. Должен появиться invoice на 10 Stars

### Если invoice НЕ появился
В логах должно быть:
```
ERROR: Invoice could not be sent
```

Это значит **Stars недоступны в вашем регионе**.

### Если invoice появился, но оплата не проходит
В логах при оплате должно быть:
```
Payment received: ...
Payment invoice: stars_...
Payment total amount: 10
Payment currency: XTR
✅ Stars payment successful!
```

## Шаг 4: Проверьте списание Stars

После успешной оплаты:
1. Проверьте баланс Stars в Telegram (настройки)
2. Звёзды должны списаться
3. Коины должны добавиться в игру

## Если Stars НЕ списываются

### Вариант 1: Stars недоступны
Вернитесь к внутриигровым коинам (как было раньше)

### Вариант 2: Ошибка в коде
Проверьте логи на наличие ошибок:
```bash
journalctl -u quantum-nexus-bot | grep ERROR
```

### Вариант 3: Тестовый режим
Если нужно тестировать без реальных Stars, скажите мне и я добавлю тестовый режим.



