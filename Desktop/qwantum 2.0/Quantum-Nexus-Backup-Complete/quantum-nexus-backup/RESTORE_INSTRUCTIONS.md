# Инструкции по восстановлению Quantum Nexus

## 📁 Расположение резервной копии
```
C:\Users\SmartFix\Desktop\qwantum 2.0\quantum-nexus-backup-2025-10-29-06-12\
```

## 🔄 Команды для восстановления

### 1. Остановка текущих сервисов (на сервере)
```bash
sudo systemctl stop quantum-nexus-web
sudo systemctl stop quantum-nexus-bot
```

### 2. Создание резервной копии текущего состояния
```bash
cd /root
cp -r quantum-nexus quantum-nexus-current-backup-$(date +%Y-%m-%d-%H-%M)
```

### 3. Восстановление из резервной копии
```bash
# Удаление текущей папки (если нужно)
rm -rf /root/quantum-nexus

# Копирование из резервной копии
# Замените путь на актуальный путь к вашей резервной копии
scp -r "C:\Users\SmartFix\Desktop\qwantum 2.0\quantum-nexus-backup-2025-10-29-06-12\quantum-nexus" root@your-server-ip:/root/
```

### 4. Установка прав доступа
```bash
cd /root/quantum-nexus
chmod +x *.sh
chmod 644 *.py *.html *.md
```

### 5. Обновление веб-файлов
```bash
sudo cp web_app.html /var/www/quantum-nexus/
sudo cp admin.html /var/www/quantum-nexus/
sudo chown -R www-data:www-data /var/www/quantum-nexus/
```

### 6. Перезапуск сервисов
```bash
sudo systemctl start quantum-nexus-web
sudo systemctl start quantum-nexus-bot
```

### 7. Проверка статуса
```bash
sudo systemctl status quantum-nexus-web
sudo systemctl status quantum-nexus-bot
```

## 📋 Альтернативный способ (если есть доступ к серверу)

### Через SCP (с Windows)
```cmd
scp -r "C:\Users\SmartFix\Desktop\qwantum 2.0\quantum-nexus-backup-2025-10-29-06-12\quantum-nexus" root@your-server-ip:/root/
```

### Через WinSCP или FileZilla
1. Подключитесь к серверу
2. Загрузите папку `quantum-nexus` из резервной копии в `/root/`
3. Выполните команды 4-7 из раздела выше

## ⚠️ Важные заметки

1. **Дата создания резервной копии**: 29.10.2025 06:12
2. **Содержимое**: Полная копия папки quantum-nexus со всеми файлами
3. **Размер**: ~1882 файла (включая .git репозиторий)
4. **Версия**: Стабильная рабочая версия без экспериментальных изменений

## 🔍 Проверка после восстановления

1. Откройте веб-приложение в браузере
2. Проверьте работу всех функций:
   - Тапы
   - Магазин
   - Майнинг
   - Карточки
   - Реферальная система
3. Проверьте админ панель
4. Убедитесь, что бот отвечает в Telegram

## 📞 Поддержка

Если возникнут проблемы при восстановлении, проверьте:
- Права доступа к файлам
- Логи сервисов: `journalctl -u quantum-nexus-web -f`
- Конфигурацию базы данных
- Настройки nginx/apache
