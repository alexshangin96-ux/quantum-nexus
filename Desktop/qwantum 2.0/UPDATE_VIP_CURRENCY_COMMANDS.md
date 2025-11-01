# 🚀 Команды для обновления VIP стиля "Купить валюту" на Selectel

**Дата:** 01.11.2025  
**Изменения:** VIP стилизация секции "Купить валюту"

## 📋 БЫСТРОЕ ОБНОВЛЕНИЕ (Одна команда)

```bash
cd /root/quantum-nexus && git pull origin main && sudo cp web_app.html /var/www/quantum-nexus/web_app.html && sudo systemctl restart quantum-nexus-web.service && sudo systemctl restart quantum-nexus && echo "✅ Обновление завершено!"
```

---

## 📝 ПОШАГОВЫЕ КОМАНДЫ

### 1️⃣ Подключение к серверу
```bash
ssh root@your-server-ip
```

### 2️⃣ Переход в папку проекта
```bash
cd /root/quantum-nexus
```

### 3️⃣ Получение последних изменений
```bash
git pull origin main
```

### 4️⃣ Копирование обновленного web_app.html
```bash
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
```

### 5️⃣ Перезапуск сервисов
```bash
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus
```

### 6️⃣ Проверка статуса
```bash
sudo systemctl status quantum-nexus-web.service
sudo systemctl status quantum-nexus
```

---

## 🔍 ПРОВЕРКА ИЗМЕНЕНИЙ

### Проверить версию файла:
```bash
head -n 5 /var/www/quantum-nexus/web_app.html
```

### Проверить логи:
```bash
sudo journalctl -u quantum-nexus-web.service -f
sudo journalctl -u quantum-nexus.service -f
```

### Проверить, что изменения загружены:
```bash
grep -A 2 "КУПИТЬ ВАЛЮТУ" /var/www/quantum-nexus/web_app.html
```

Должно быть:
```html
<h2 style="font-size: 26px; color: #000; margin: 0; font-weight: 900;">⭐ КУПИТЬ ВАЛЮТУ</h2>
```

---

## ✨ ЧТО БЫЛО ИЗМЕНЕНО

### 1. VIP Золотой заголовок
- ✅ Градиентный золотой фон (#ffd700 → #ffed4e)
- ✅ Чёрный текст с font-weight: 900
- ✅ Золотая рамка и тень вокруг модального окна

### 2. Кнопки категорий
- ✅ Font-weight: 900 для всех кнопок
- ✅ Тени по категориям
- ✅ Улучшенная читаемость

### 3. Карточки товаров (60+ штук)
- ✅ Градиентный фон по категориям
- ✅ VIP тени для глубины
- ✅ Автоматическое применение стилей через JavaScript

### 4. Цветовые схемы
- 🎯 Старт: Синий #667eea
- 🚀 Премиум: Золотой #f59e0b
- ⭐ VIP: Золотой VIP #ffd700
- 🔮 QuanHash: Красный #ff0000
- 🎁 Комбо: Фиолетовый #800080
- 👑 VIP функции: Золотой VIP #ffd700

---

## 🆘 ЕСЛИ ЧТО-ТО ПОШЛО НЕ ТАК

### Откат к предыдущей версии:
```bash
cd /root/quantum-nexus
git reset --hard HEAD~1
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus
```

### Проверка изменений перед откатом:
```bash
git log --oneline -5
git diff HEAD~1 web_app.html
```

---

## ✅ ПРОВЕРКА РАБОТЫ

После обновления проверьте:
1. Откройте бота в Telegram
2. Перейдите в меню
3. Нажмите "⭐ Купить валюту"
4. Убедитесь, что:
   - Золотой заголовок отображается
   - Кнопки категорий стильные
   - Все карточки с градиентами и тенями
   - VIP стиль работает корректно

---

## 📊 СТАТУС

✅ Изменения загружены в Git  
✅ Готовы к развертыванию на Selectel  
✅ Бэкап создан: `Quantum-Nexus-Backup-2025-11-01-16-23`

**Дата изменений:** 01.11.2025  
**Версия:** Quantum Nexus v4.3

