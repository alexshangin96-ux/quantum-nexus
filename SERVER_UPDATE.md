# 🚀 КОМАНДЫ ДЛЯ ОБНОВЛЕНИЯ СЕРВЕРА

## 📋 Полный процесс обновления

### Вариант 1: Автоматический скрипт (РЕКОМЕНДУЕТСЯ)

```bash
# На сервере выполните:
cd ~/quantum-nexus
bash UPDATE_VIP_NOW.sh
```

### Вариант 2: Ручное обновление (пошагово)

#### 1. Подключитесь к серверу
```bash
ssh root@your-server-ip
# или
ssh user@your-server-ip
```

#### 2. Перейдите в директорию проекта
```bash
cd ~/quantum-nexus
# или
cd /root/quantum-nexus
```

#### 3. Получите последние изменения
```bash
git pull origin main
```

#### 4. Скопируйте обновленный файл
```bash
sudo cp web_app.html /var/www/quantum-nexus/
```

#### 5. Перезапустите сервисы
```bash
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus
```

#### 6. Проверьте статус
```bash
sudo systemctl status quantum-nexus-web.service
sudo systemctl status quantum-nexus
```

---

## ✅ Что обновилось

### VIP Функции:
- ✨ Премиальный VIP фон
- 👤 Профиль с загрузкой фото (справа)
- 🏆 Топ лидеры с полной статистикой (слева)
- 💰 VIP бусты x20 и x50
- 🎉 VIP турниры и события
- 💳 VIP карточки
- 💸 VIP бонусы при выводе (0% комиссия)
- ✨ VIP визуальные эффекты
- 🤖 VIP машины

### Все файлы:
- `web_app.html` - обновлен
- `web_server.py` - добавлены API endpoints
- `admin.html` - VIP управление

---

## 🔍 Быстрая проверка

После обновления проверьте:

1. **Откройте бота** и используйте `/start`
2. **Проверьте VIP кнопки:**
   - Слева сверху: 🏆 Топ лидеры
   - Справа сверху: 👤 Профиль

3. **Проверьте VIP функции:**
   - VIP бусты в магазине
   - VIP турниры в заданиях
   - VIP карточки
   - VIP бонусы при выводе

---

## 🆘 Если что-то не работает

### Сброс кеша:
```bash
# На сервере:
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus
```

### Проверка логов:
```bash
sudo journalctl -u quantum-nexus-web.service -f
sudo journalctl -u quantum-nexus -f
```

### Принудительный пул:
```bash
cd ~/quantum-nexus
git fetch origin
git reset --hard origin/main
sudo cp web_app.html /var/www/quantum-nexus/
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus
```

---

## 📝 Полный список команд одной строкой

```bash
cd ~/quantum-nexus && git pull origin main && sudo cp web_app.html /var/www/quantum-nexus/ && sudo systemctl restart quantum-nexus-web.service && sudo systemctl restart quantum-nexus && echo "✅ Обновление завершено!"
```

---

## 🎉 Готово!

После выполнения команд:
1. Все VIP функции будут активны
2. Профиль с загрузкой фото работает
3. Топ лидеры отображаются
4. VIP бусты доступны
5. Все визуальные эффекты применены

**Не забудьте использовать `/start` в боте для обновления кеша!**






