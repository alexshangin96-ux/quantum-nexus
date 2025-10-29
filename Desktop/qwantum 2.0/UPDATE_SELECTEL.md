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

### 3. Обновление кода из GitHub
```bash
git pull origin master
```

### 4. Копирование обновленных файлов
```bash
# Копируем обновленный web_app.html в веб-папку
sudo cp web_app.html /var/www/quantum-nexus/web_app.html

# Копируем обновленный web_server.py
sudo cp web_server.py /root/quantum-nexus/
```

### 5. Перезапуск сервисов
```bash
# Перезапускаем веб-сервис
sudo systemctl restart quantum-nexus-web.service

# Перезапускаем основной сервис бота
sudo systemctl restart quantum-nexus.service
```

### 6. Проверка статуса
```bash
# Проверка статуса сервисов
sudo systemctl status quantum-nexus-web.service
sudo systemctl status quantum-nexus.service

# Проверка логов
sudo journalctl -u quantum-nexus.service -f
sudo journalctl -u quantum-nexus-web.service -f
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

## 🚀 Быстрые команды (копируйте и вставляйте)

```bash
cd /root/quantum-nexus
git pull origin master
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo cp web_server.py /root/quantum-nexus/
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service
```

## 🆘 Если что-то пошло не так

1. Проверьте логи: `sudo journalctl -u quantum-nexus.service -f`
2. Проверьте статус: `sudo systemctl status quantum-nexus.service`
3. Откатитесь к предыдущей версии: `git reset --hard HEAD~1`
4. Перезапустите сервисы: `sudo systemctl restart quantum-nexus-web.service && sudo systemctl restart quantum-nexus.service`
