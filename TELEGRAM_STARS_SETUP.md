# Настройка Telegram Stars для покупки валюты

## Что требуется от вас:

### 1. Активация Stars в Bot API
Вы правы — **токен не требуется**! Telegram Stars работает через встроенный API Telegram.

### 2. Создание invoice в боте
Нужно создать invoice в вашем боте через Telegram Bot API:

```bash
# В вашем боте используйте метод createInvoice
# Пример: создать invoice в боте (handlers.py или отдельный скрипт)
```

### 3. Подготовка invoice
Для каждого товара создайте invoice через бот:
- `stars_pack_1` — для стартового пакета (10 ⭐)
- `stars_pack_2` — для премиум пакета (40 ⭐)

## Команды для создания invoice

Добавьте в handlers.py функцию создания invoice:

```python
import requests

def create_stars_invoice(bot, user_id, amount, description):
    """Create Stars invoice"""
    invoice = {
        "currency": "XTR",  # Telegram Stars
        "prices": [
            {
                "label": description,
                "amount": amount * 100  # Amount in stars (convert to smallest unit)
            }
        ]
    }
    
    # Create invoice via Bot API
    result = bot.create_invoice_link(
        title=description,
        description=f"Покупка {description}",
        payload=f"stars_pack_{user_id}",
        provider_token="",  # Not needed for Stars
        currency="XTR",
        prices=invoice["prices"]
    )
    
    return result
```

## Настройка invoice в боте

1. Откройте **@BotFather** в Telegram
2. Выберите вашего бота
3. Зайдите в **Monetization** → **Invoices**
4. Создайте invoice для каждого товара

Альтернативный способ — создать invoice программно в handlers.py перед отображением кнопки "Купить валюту".

## Полная реализация требует:

1. **Создать invoice в боте** перед открытием модального окна
2. **Получить invoice URL** и передать его в `tg.openInvoice()`
3. **Верифицировать платеж** на бэкенде после получения статуса "paid"

## Быстрый старт:

Добавьте эту функцию в handlers.py:

```python
@bot.message_handler(commands=['buy_stars'])
def buy_stars(message):
    # Create invoice
    result = bot.create_invoice_link(
        title="Купить коины",
        description="Покупка через Stars",
        payload="stars_pack_1",
        currency="XTR",
        prices=[types.LabeledPrice(label="1M коинов", amount=1000)]  # 10 stars = 1000
    )
    
    bot.send_message(
        message.chat.id,
        f"💰 Купить за Stars:\n{result}"
    )
```





