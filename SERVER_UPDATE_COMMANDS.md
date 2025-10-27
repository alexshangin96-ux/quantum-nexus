# Команды для обновления сервера Quantum Nexus

## ✅ Все изменения выполнены!

### Что было сделано:
1. ✅ Ускорено автообновление до 2 секунд
2. ✅ Добавлена красивая SVG кнопка тапа
3. ✅ Улучшены анимации покупок
4. ✅ Добавлено 30 уникальных карточек
5. ✅ Реализована система ежедневных заданий
6. ✅ Добавлена кнопка "💬 Вопросы" в админку
7. ✅ Исправлена реферальная ссылка
8. ✅ Добавлен цветовой эффект при нажатии на кнопку тапа

## 🚀 Команды для обновления

### 1. Обновить код на сервере:
```bash
cd /root/quantum-nexus
git pull origin main
```

### 2. Обновить файлы приложения:
```bash
cp web_app.html /var/www/quantum-nexus/
cp admin.html /var/www/quantum-nexus/
cp web_server.py /root/quantum-nexus/
cp models.py /root/quantum-nexus/
```

### 3. Обновить базу данных (добавить поля):
```bash
sudo -u postgres psql quantum_nexus
```

В PostgreSQL консоли выполните:
```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_passive_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hash_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS referral_code VARCHAR(50);
SELECT * FROM users LIMIT 1;
\q
```

### 4. Установить зависимости (если нужно):
```bash
cd /root/quantum-nexus
source venv/bin/activate
pip install -q sqlalchemy flask flask-cors python-dotenv python-telegram-bot
```

### 5. Перезапустить сервисы:
```bash
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx
```

### 6. Проверить статус:
```bash
sudo systemctl status quantum-nexus
sudo systemctl status quantum-nexus-web
sudo systemctl status nginx
```

### 7. Посмотреть логи (если есть ошибки):
```bash
sudo journalctl -u quantum-nexus -f
sudo journalctl -u quantum-nexus-web -f
```

## 📝 Проверка работы

1. Откройте бота в Telegram: https://t.me/Quanexus_bot
2. Нажмите кнопку "🎮 Открыть игру"
3. Проверьте:
   - Кнопку тапа с эффектом цвета
   - Анимации покупок
   - Раздел "Карточки" с 30 позициями
   - Раздел "Бонусы" (ежедневные задания)
   - Реферальную ссылку

4. Откройте админ-панель: https://quantum-nexus.ru/admin
5. Проверьте раздел "💬 Вопросы"

## 🔧 Если что-то не работает

### Ошибка в логах:
```bash
sudo journalctl -u quantum-nexus-web -n 50 --no-pager
```

### Обновить все файлы принудительно:
```bash
cd /root/quantum-nexus
git fetch origin
git reset --hard origin/main
git clean -fd
```

### Пересоздать базу данных (ОСТОРОЖНО - удалит данные):
```bash
cd /root/quantum-nexus
python3 -c "from database import init_db; init_db()"
```

## ✨ Готово!

Все изменения применены. Приложение готово к использованию!


