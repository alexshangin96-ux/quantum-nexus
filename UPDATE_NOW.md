# Команды для обновления на сервере

## Быстрое обновление

```bash
ssh root@ваш_IP
cd /root/quantum-nexus
git pull origin main
systemctl restart quantum-nexus-bot
systemctl restart quantum-nexus-web
```

## Проверка работы

1. Откройте бота: @qanexus_bot
2. Откройте веб-приложение
3. Нажмите "Купить валюту"
4. Выберите товар и нажмите "Купить"
5. Подтвердите в боте

## Что изменилось

- **Имя бота обновлено**: @qanexus_bot
- **Система оплаты**: Использует внутриигровые коины вместо Stars
- **Товары**:
  - 1,000,000 коинов за 100 коинов
  - 5,000,000 коинов за 500 коинов

## Логи

```bash
# Проверить логи бота
journalctl -u quantum-nexus-bot -f

# Проверить веб-сервер
journalctl -u quantum-nexus-web -f
```

