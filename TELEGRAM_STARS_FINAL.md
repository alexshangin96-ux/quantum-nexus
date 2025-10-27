# Полная интеграция Telegram Stars

## Что реализовано

### 1. **Реальная оплата через Telegram Stars API**

Система использует официальный Telegram Bot API для оплаты через Stars:

```python
# Отправка invoice
await context.bot.send_invoice(
    chat_id=update.effective_chat.id,
    title=f"💎 {product['title']}",
    description=product['description'],
    payload=f"stars_{user.id}_{product_id}",
    provider_token="",  # Пустая строка для Stars
    currency="XTR",  # Stars валюта
    prices=[LabeledPrice(
        label=f"{product['title']} - {product['description']}",
        amount=product['stars']
    )]
)
```

### 2. **Валидация платежа**

- `pre_checkout_handler` - проверяет пользователя перед оплатой
- `successful_payment_handler` - обрабатывает успешную оплату и добавляет коины

### 3. **Товары**

- **Стартовый пакет**: 10 ⭐ → 1,000,000 коинов
- **Премиум пакет**: 40 ⭐ → 5,000,000 коинов

## Важно! Настройка Stars

### Telegram Stars доступны только в определенных регионах

**Регионы с поддержкой Stars:**
- США
- Япония
- Южная Корея
- И другие (обновляется Telegram)

### Как включить Stars для вашего бота

1. **Не нужно ничего включать в BotFather**
   - Stars работают автоматически через Bot API
   - Просто используйте `currency="XTR"` и `provider_token=""`

2. **Важно**: Сумма в `amount` должна быть в **типах** (как в примере)

### Проверка доступности Stars

Если Stars недоступны в вашем регионе, invoice не отобразится пользователю.

## Развертывание

```bash
ssh root@ваш_IP
cd /root/quantum-nexus
git pull origin main
systemctl restart quantum-nexus-bot
systemctl restart quantum-nexus-web
```

## Как работает

1. Пользователь нажимает "Купить валюту" в веб-приложении
2. Открывается бот `@qanexus_bot` с командой `/start buy_stars_1`
3. Бот отправляет invoice с оплатой в Stars
4. Пользователь оплачивает Stars через Telegram
5. Telegram проверяет платеж (`pre_checkout_handler`)
6. Telegram отправляет подтверждение (`successful_payment_handler`)
7. Коины добавляются пользователю

## Тестирование

1. Убедитесь, что вы в регионе с поддержкой Stars
2. Откройте бота @qanexus_bot
3. Отправьте `/start buy_stars_1`
4. Должен появиться invoice на оплату
5. Оплатите Stars
6. Коины добавятся автоматически

## Логи

```bash
# Проверить логи бота
journalctl -u quantum-nexus-bot -f

# Проверить успешные платежи
journalctl -u quantum-nexus-bot | grep "bought product"
```

## Ошибки

### "Invoice не отображается"
- Проверьте, что вы в регионе с поддержкой Stars
- Проверьте логи: `journalctl -u quantum-nexus-bot -f`

### "provider_token is required"
- Убедитесь, что используете `provider_token=""` (пустая строка)
- Убедитесь, что `currency="XTR"`

### "Amount must be a positive integer"
- `amount` должен быть целым числом (например, 10, а не 10.0)

## Безопасность

- Payload включает `user.id` для защиты от подделок
- Проверка пользователя при успешной оплате
- Логирование всех покупок

## Альтернатива (если Stars недоступны)

Если Stars недоступны в вашем регионе, можно вернуться к использованию внутриигровых коинов (как было ранее).

Измените в `handlers.py` функцию `send_stars_invoice`:
- Вместо отправки invoice, проверьте баланс и спишите коины
- Добавьте бонусные коины

