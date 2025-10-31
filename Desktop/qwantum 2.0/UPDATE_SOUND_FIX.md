# 🔊 Команды для обновления исправлений звука на Selectel

## 📋 Пошаговые команды для обновления web_app.html

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
git pull origin main
```

### 4. Копирование обновленного файла
```bash
# Копируем обновленный web_app.html в веб-папку
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
```

### 5. Перезапуск веб-сервиса
```bash
# Перезапускаем веб-сервис
sudo systemctl restart quantum-nexus-web.service
```

### 6. Проверка статуса
```bash
# Проверка статуса веб-сервиса
sudo systemctl status quantum-nexus-web.service

# Проверка логов (Ctrl+C для выхода)
sudo journalctl -u quantum-nexus-web.service -f
```

## 🚀 Быстрые команды (копируйте и вставляйте)
```bash
cd /root/quantum-nexus && git pull origin main && sudo cp web_app.html /var/www/quantum-nexus/web_app.html && sudo systemctl restart quantum-nexus-web.service
```

## 📝 Что было исправлено
1. **Звук и вибрация теперь по умолчанию выключены**
   - Теперь пользователь должен явно включить их в настройках
   - Исправлена логика проверки: было `!== 'false'`, стало `=== 'true'`

2. **Исправлена обработка AudioContext в suspended состоянии**
   - Добавлен `audioContext.resume()` для автоматического возобновления
   - Улучшена обработка ошибок при создании AudioContext

3. **Обновлена логика в настройках**
   - По умолчанию переключатели звука и вибрации выключены
   - При первом открытии настроек они будут показывать выключенное состояние

## ✅ Проверка работы после обновления
1. Откройте приложение в Telegram
2. Зайдите в Настройки ⚙️
3. Убедитесь, что переключатели звука и вибрации **выключены**
4. Включите звук и вибрацию
5. Сохраните настройки
6. Попробуйте сделать тап - должны работать и звук и вибрация

## 🆘 Если что-то пошло не так
1. Проверьте логи: `sudo journalctl -u quantum-nexus-web.service -n 50`
2. Проверьте статус: `sudo systemctl status quantum-nexus-web.service`
3. Посмотрите последний коммит: `git log --oneline -3`
4. Откатитесь к предыдущей версии: `git reset --hard HEAD~1` и повторите шаги 4-5

