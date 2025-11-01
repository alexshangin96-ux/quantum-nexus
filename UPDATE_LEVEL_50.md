# Обновление до уровня 50 для майнинг машин v6.1

## ✅ Что изменено

1. **Лимит уровня 50** для всех майнинг машин (обычные и VIP)
2. **Визуальные индикаторы** максимального уровня:
   - Показатель уровня: "Уровень X / 50" или "Уровень 50 ⭐ MAX"
   - Кнопка покупки меняется на "✨ Максимальный уровень" (золотого цвета)
   - Отключение покупки при достижении лимита
3. **Проверка лимита** на сервере при покупке машин
4. **Поддержка категории VIP** в API майнинга

## 📦 Файлы изменены

- `web_app.html` - фронтенд с визуальными индикаторами и лимитом
- `web_server.py` - проверка лимита при покупке
- `handlers.py` - обработка VIP машин майнинга
- `models.py` - поля mining_vip_levels уже добавлены ранее

## 🚀 Команды для обновления на сервере

```bash
cd /root/quantum-nexus

# 1. Получить последние изменения
git pull origin main

# 2. Обновить файлы приложения
sudo cp quantum-nexus/web_app.html /var/www/quantum-nexus/web_app.html
sudo cp quantum-nexus/web_server.py /root/quantum-nexus/web_server.py
sudo cp quantum-nexus/handlers.py /root/quantum-nexus/handlers.py

# 3. Перезапустить сервисы
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service

# 4. Проверить статус
sudo systemctl status quantum-nexus-web.service
sudo systemctl status quantum-nexus.service

# 5. Посмотреть логи (если есть ошибки)
journalctl -u quantum-nexus-web.service -f
journalctl -u quantum-nexus.service -f
```

## 💰 Примеры прогрессии цен с лимитом 50

**CPU Майнер (база 5,000 коинов, 10 QuanHash/ч):**
- Уровень 1: 5,750 коинов, 12 QuanHash/ч
- Уровень 25: 318,100 коинов, 362 QuanHash/ч
- **Уровень 50: 10,120,000 коинов, 10,836 QuanHash/ч ⭐ MAX**

**VIP Quantum Prime (база 50 Stars, 120,000 QuanHash/ч):**
- Уровень 1: 58 Stars, 138,000 QuanHash/ч
- Уровень 25: 3,181 Stars, 4,341,000 QuanHash/ч
- **Уровень 50: 101,200 Stars, 1,300,000,000 QuanHash/ч ⭐ MAX**

## ✨ Особенности

- Множитель цены: 1.15x (уменьшен с 1.2x для баланса)
- Множитель дохода: 1.15x
- Максимальный уровень: 50
- Визуальная индикация при достижении лимита
- Проверка на сервере и фронтенде


