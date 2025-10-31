# 🔊 Команды для обновления системы звуков Crypto Tapping

## ⚠️ МАЖОРНОЕ ОБНОВЛЕНИЕ ЗВУКОВОЙ СИСТЕМЫ!

Добавлено **20 новых звуков** в стиле Crypto Tapping!

---

## 🚀 БЫСТРАЯ КОМАНДА:

```bash
cd /root/quantum-nexus && git pull origin main && sudo cp web_app.html /var/www/quantum-nexus/web_app.html && sudo systemctl restart quantum-nexus-web.service
```

---

## 📋 Пошаговые команды:

```bash
ssh root@your-server-ip
cd /root/quantum-nexus
git pull origin main
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo systemctl restart quantum-nexus-web.service
sudo systemctl status quantum-nexus-web.service
```

---

## 🎵 Новые звуки (всего 35 звуков!):

### Основные звуки (было):
1. `tap` - Тап по экрану
2. `coin` - Монета
3. `levelup` - Повышение уровня
4. `error` - Ошибка
5. `success` - Успех
6. `purchase` - Покупка
7. `mining` - Майнинг
8. `card` - Карточка
9. `energy_regen` - Восстановление энергии
10. `achievement` - Достижение
11. `click_boost` - Клик буст
12. `vip_levelup` - Повышение VIP
13. `collection` - Сбор коллекции
14. `bonus` - Бонус

### Новые звуки Crypto Tapping (20 звуков):
15. `crypto_tap` - 💰 Крипто тап (падение денег)
16. `big_coin` - 💎 Большая монета (удовлетворительный чинг)
17. `stars_collect` - ⭐ Сбор звезд (магическая искра)
18. `machine_working` - 🔧 Работа машины (глубокий гул)
19. `rebirth` - 🔄 Ребирт (драматическая трансформация)
20. `powerup` - ⚡ Пауэрап (энергетический всплеск)
21. `critical_hit` - 💥 Критический удар (взрывной бум)
22. `level_milestone` - 🎯 Веха уровня (фанфары)
23. `combo` - 🔥 Комбо (растущая высота)
24. `daily_bonus` - 📅 Ежедневный бонус (празднование)
25. `shop_hover` - 🏪 Наведение в магазине (тик)
26. `scroll` - 📜 Скролл (плавный свайп)
27. `notification` - 🔔 Уведомление (мягкий пинг)
28. `wrong_action` - ❌ Неправильное действие (жужжание)
29. `open_menu` - 📂 Открытие меню (свист)
30. `close_menu` - 📁 Закрытие меню (обратный свист)
31. `click` - 👆 Клик (базовый клик)

### ⚡ Производные звуки (4):
32. `energy_boost` - Использует `powerup`
33. `rarity_unlock` - Использует `achievement`
34. `multiplier_active` - Использует `combo`
35. `jackpot` - Использует `big_coin`

---

## 🎮 Куда добавить звуки в игре:

### Интерфейс:
- `click` - При любом клике по кнопке
- `open_menu` - При открытии любого меню
- `close_menu` - При закрытии меню
- `scroll` - При скролле списков
- `shop_hover` - При наведении на товар в магазине
- `notification` - При уведомлении

### Основная механика:
- `tap` - Обычный тап
- `crypto_tap` - Тап с крипто бонусом
- `coin` - Обычная монета
- `big_coin` - Большая монета/джекпот
- `combo` - При комбо
- `critical_hit` - При критическом тапе

### Майнинг:
- `mining` - Покупка майнера
- `machine_working` - При работе майнинг машин

### Покупки:
- `purchase` - Обычная покупка
- `card` - Покупка карты
- `energy_regen` - Восстановление энергии
- `powerup` - Активация буста

### Достижения:
- `levelup` - Повышение уровня
- `level_milestone` - Веха уровня (каждые 10-50 уровней)
- `achievement` - Разблокировка достижения
- `vip_levelup` - Повышение VIP
- `daily_bonus` - Ежедневный бонус
- `rebirth` - Ребирт

### Ошибки:
- `error` - Ошибка
- `wrong_action` - Неправильное действие

---

## ⚙️ Как использовать звуки:

### Пример в коде:
```javascript
// Просто вызовите playSound с нужным типом
playSound('crypto_tap');
playSound('big_coin');
playSound('level_milestone');
```

### Все звуки проверяют настройку:
```javascript
const soundSetting = localStorage.getItem('soundEnabled');
const soundEnabled = soundSetting === 'true';
if (!soundEnabled) return; // Звук отключен
```

---

## 🔧 Настройки звука:

### По умолчанию:
- **Звук ВЫКЛЮЧЕН** ❌
- Пользователь должен включить в настройках

### В настройках:
1. Откройте ⚙️ Настройки
2. Найдите 🔊 ЗВУК И ВИБРАЦИЯ
3. Включите переключатель **Звуки**
4. Нажмите **Сохранить**

### Переключатель управляет:
- ✅ ВСЕМИ звуками сразу
- ✅ Если ВЫКЛЮЧЕН - звуков НЕТ вообще
- ✅ Если ВКЛЮЧЕН - работают ВСЕ звуки

---

## ✅ Проверка после обновления:

1. Откройте приложение в Telegram
2. Зайдите в Настройки ⚙️
3. Включите звуки (переключатель синий)
4. Сохраните настройки
5. Должен прозвучать `success`
6. Попробуйте тап - должен звучать `tap`
7. Откройте магазин - должен звучать `open_menu`
8. Закройте магазин - должен звучать `close_menu`

---

## 🐛 Отладка:

### Все логи активны:
```javascript
Sound toggle changed: true
saveSettings - soundEnabled: true hapticsEnabled: true
Playing sound: success
AudioContext created, state: suspended
AudioContext resumed successfully, state: running
Creating oscillator for sound: success
Sound started successfully: success
```

### Проверьте в консоли браузера:
```javascript
// Проверьте настройку звука
localStorage.getItem('soundEnabled')

// Проверьте состояние AudioContext
window.audioContext?.state

// Попробуйте воспроизвести звук вручную
playSound('crypto_tap');
```

---

## 📊 История изменений:

### Коммит 3b07390:
- ✅ Добавлено 20 новых звуков
- ✅ Все звуки в стиле Crypto Tapping
- ✅ Разнообразная палитра: от крипто до UI
- ✅ Звуки охватывают всю механику игры

---

## 🎯 Следующие шаги:

1. Обновите сервер (команды выше)
2. Протестируйте все звуки
3. Добавьте вызовы `playSound()` в нужные места игры
4. Убедитесь, что переключатель правильно работает
5. После теста - **удалите логи** для продакшена

---

## 📝 Рекомендации по интеграции:

### Приоритет 1 (основные звуки):
- `tap` - уже есть ✅
- `purchase` - уже есть ✅
- `levelup` - уже есть ✅
- `achievement` - уже есть ✅

### Приоритет 2 (интерфейс):
- `open_menu` - добавить в открытие модалок
- `close_menu` - добавить в закрытие модалок
- `click` - добавить в кнопки
- `scroll` - добавить в скролл

### Приоритет 3 (особые события):
- `level_milestone` - при больших достижениях
- `combo` - при комбо
- `critical_hit` - при критических ударах
- `daily_bonus` - при ежедневных бонусах
- `rebirth` - при ребирте
- `machine_working` - при работе майнинг машин

### Приоритет 4 (атмосфера):
- `stars_collect` - сбор звезд
- `shop_hover` - наведение в магазине
- `notification` - уведомления
- `wrong_action` - ошибки
- `crypto_tap` - крипто тапы
- `big_coin` - большие монеты

---

## 🆘 Поддержка:

Если звуки не работают:
1. Проверьте логи в консоли браузера
2. Убедитесь, что звук включен в настройках
3. Проверьте AudioContext в консоли
4. Посмотрите `FINAL_SOUND_FIX_COMMANDS.md` для отладки

---

**ВАЖНО**: Сейчас работает ПОЛНОЕ ЛОГИРОВАНИЕ! После проверки удалите логи.

