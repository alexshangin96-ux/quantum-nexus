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

### Версия 1 (коммит 5a46aac)
1. **Звук и вибрация теперь по умолчанию выключены**
   - Теперь пользователь должен явно включить их в настройках
   - Исправлена логика проверки: было `!== 'false'`, стало `=== 'true'`

2. **Исправлена обработка AudioContext в suspended состоянии**
   - Добавлен `audioContext.resume()` для автоматического возобновления
   - Улучшена обработка ошибок при создании AudioContext

3. **Обновлена логика в настройках**
   - По умолчанию переключатели звука и вибрации выключены
   - При первом открытии настроек они будут показывать выключенное состояние

### Версия 2 (коммит 667e14a) - Отладка
4. **Добавлено подробное логирование для диагностики звука**
   - Логи показывают состояние AudioContext
   - Логи показывают значение soundEnabled при сохранении настроек
   - Логи показывают каждый шаг воспроизведения звука
   - Логи показывают когда звук отключен и почему

5. **Исправлены проверки в saveSettings**
   - Изменено `soundEnabled !== false` на `soundEnabled === true` для строгой проверки

## ✅ Проверка работы после обновления
1. Откройте приложение в Telegram
2. Зайдите в Настройки ⚙️
3. Убедитесь, что переключатели звука и вибрации **выключены**
4. Включите звук и вибрацию
5. Сохраните настройки
6. Попробуйте сделать тап - должны работать и звук и вибрация

## 🆘 Если что-то пошло не так / Отладка звука

### На сервере:
1. Проверьте логи: `sudo journalctl -u quantum-nexus-web.service -n 50`
2. Проверьте статус: `sudo systemctl status quantum-nexus-web.service`
3. Посмотрите последний коммит: `git log --oneline -3`
4. Откатитесь к предыдущей версии: `git reset --hard HEAD~1` и повторите шаги 4-5

### В браузере/Telegram WebView:
1. Откройте консоль разработчика в приложении (через DevTools или удаленную отладку)
2. Проверьте логи в консоли при:
   - Открытии настроек: должно быть `saveSettings - soundEnabled: true/false`
   - Сохранении настроек: должно быть `Saved soundEnabled to localStorage: true/false`
   - Попытке воспроизвести звук: должна быть серия логов от `playSound`
3. Проверьте значение в localStorage:
   ```javascript
   localStorage.getItem('soundEnabled')  // Должно быть 'true' или 'false'
   ```
4. Проверьте состояние AudioContext:
   ```javascript
   // В консоли браузера
   window.audioContext?.state  // Должно быть 'running' или 'suspended'
   ```

### Частые проблемы:
- **"Sound disabled, setting: null"** - Пользователь не включил звук в настройках (это нормально)
- **"Sound disabled, setting: false"** - Звук явно выключен в настройках
- **"AudioContext not available"** - Проблема с созданием AudioContext (возможно браузер не поддерживает)
- **"AudioContext state: suspended"** - AudioContext приостановлен, должно автоматически возобновиться

