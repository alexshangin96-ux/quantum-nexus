# 🚀 Команды для обновления на Selectel

## 📋 Пошаговые команды для обновления автобота

### 1. Подключение к серверу Selectel
```bash
ssh root@your-server-ip
```

### 2. Переход в папку проекта
```bash
cd /root/quantum-nexus
```

### 3. Остановка бота (если запущен)
```bash
pkill -f "python.*bot.py"
# или
systemctl stop quantum-nexus
```

### 4. Создание бэкапа текущей версии
```bash
cp -r /root/quantum-nexus /root/quantum-nexus-backup-$(date +%Y%m%d-%H%M%S)
```

### 5. Обновление кода из GitHub
```bash
git pull origin master
```

### 6. Установка зависимостей (если нужно)
```bash
pip install -r requirements.txt
```

### 7. Обновление базы данных (если нужно)
```bash
# Если есть миграции
python -c "from database import init_db; init_db()"
```

### 8. Запуск бота
```bash
# Запуск в фоне
nohup python bot.py > bot.log 2>&1 &

# Или через systemd
systemctl start quantum-nexus
systemctl enable quantum-nexus
```

### 9. Проверка статуса
```bash
# Проверка процессов
ps aux | grep python

# Проверка логов
tail -f bot.log

# Проверка systemd (если используется)
systemctl status quantum-nexus
```

## 🔧 Дополнительные команды

### Проверка изменений в файлах
```bash
# Проверка изменений в web_app.html
git show HEAD:quantum-nexus/web_app.html | grep -A 5 -B 5 "Купить за"
```

### Откат изменений (если что-то пошло не так)
```bash
git reset --hard HEAD~1
git push --force origin master
```

### Проверка статуса Git
```bash
git status
git log --oneline -5
```

## 📝 Что было изменено

1. **web_app.html** - Изменен текст кнопки с "Улучшить" на "Купить" для автобота
2. **web_app.html** - Добавлены ID кнопок автобота для правильной блокировки
3. **Логика блокировки** - Уже работала правильно:
   - При покупке автобота блокируются все кнопки
   - Купленная кнопка показывает таймер
   - Остальные кнопки показывают "🔒 Недоступно"

## ✅ Проверка работы

После обновления проверьте:
1. Откройте магазин в боте
2. Перейдите в раздел "Автобот"
3. Убедитесь, что кнопки показывают "Купить" вместо "Улучшить"
4. Купите автобота и проверьте блокировку кнопок
5. Убедитесь, что на купленной кнопке показывается таймер

## 🆘 Если что-то пошло не так

1. Проверьте логи: `tail -f bot.log`
2. Проверьте статус: `systemctl status quantum-nexus`
3. Откатитесь к бэкапу: `cp -r /root/quantum-nexus-backup-* /root/quantum-nexus`
4. Перезапустите бота
