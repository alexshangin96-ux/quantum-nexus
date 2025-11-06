# Обновление бота на сервере

## Команды для развертывания

```bash
ssh root@ваш_IP
cd /root/quantum-nexus
git pull origin main
systemctl restart quantum-nexus-bot
systemctl restart quantum-nexus-web
```

## Проверка логов платежей

```bash
# Смотреть логи в реальном времени
journalctl -u quantum-nexus-bot -f

# Проверить последние покупки Stars
journalctl -u quantum-nexus-bot | grep "Stars payment"

# Проверить все платежи
journalctl -u quantum-nexus-bot | grep "Payment received"
```

## Что проверить в логах

При оплате через Stars должны появиться строки:
```
Payment received: [объект платежа]
Payment invoice: stars_{user_id}_{product_id}
Payment total amount: 10 (или 40)
Payment currency: XTR
✅ Stars payment successful! User {telegram_id} bought product {id}
```

## Если Stars НЕ списываются

### 1. Проверьте, что invoice отправляется
Откройте бота и отправьте `/start buy_stars_1`

Должен появиться invoice на оплату 10 Stars

### 2. Проверьте регион
Telegram Stars работают только в определенных регионах:
- США
- Япония
- Южная Корея
- И другие

### 3. Если invoice НЕ появляется
В логах должно быть:
```
Error: Invoice could not be sent
```

Это значит Stars недоступны в вашем регионе.

## Исправление проблемы

Если Stars недоступны, можно:
1. Вернуться к системе внутриигровых коинов
2. Или использовать тестовый режим (добавлю команду для теста)

## Тестовый режим (без реальной оплаты)

Если нужно протестировать без реальных Stars:
- Откройте бота
- Отправьте `/start buy_stars_1`
- Закройте invoice (не оплачивайте)
- Бот покажет сообщение о покупке (в тестовом режиме)










