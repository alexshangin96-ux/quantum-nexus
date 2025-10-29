# Quantum Nexus - Полная резервная копия

## 📁 Содержимое резервной копии

Эта папка содержит полную резервную копию проекта Quantum Nexus на момент 29.10.2025 06:12.

### Структура:
- **quantum-nexus/** - Полная копия приложения (1885 файлов)
- **RESTORE_INSTRUCTIONS.md** - Подробные инструкции по восстановлению
- **QUICK_RESTORE.sh** - Скрипт для быстрого восстановления
- **BACKUP_INFO.txt** - Информация о резервной копии

## 🚀 Быстрое восстановление

### Windows (PowerShell):
```powershell
# Остановка сервисов
ssh root@your-server-ip "sudo systemctl stop quantum-nexus-web && sudo systemctl stop quantum-nexus-bot"

# Загрузка на сервер
scp -r "quantum-nexus-backup\quantum-nexus" root@your-server-ip:/root/

# Установка и запуск
ssh root@your-server-ip "cd /root/quantum-nexus && chmod +x *.sh && sudo cp web_app.html /var/www/quantum-nexus/ && sudo cp admin.html /var/www/quantum-nexus/ && sudo systemctl start quantum-nexus-web && sudo systemctl start quantum-nexus-bot"
```

### Linux/macOS:
```bash
# Остановка сервисов
ssh root@your-server-ip "sudo systemctl stop quantum-nexus-web && sudo systemctl stop quantum-nexus-bot"

# Загрузка на сервер
scp -r quantum-nexus-backup/quantum-nexus root@your-server-ip:/root/

# Установка и запуск
ssh root@your-server-ip "cd /root/quantum-nexus && chmod +x *.sh && sudo cp web_app.html /var/www/quantum-nexus/ && sudo cp admin.html /var/www/quantum-nexus/ && sudo systemctl start quantum-nexus-web && sudo systemctl start quantum-nexus-bot"
```

## 📋 Подробные инструкции

Смотрите файл `RESTORE_INSTRUCTIONS.md` для детальных инструкций по восстановлению.

## ⚠️ Важно

- Убедитесь, что у вас есть доступ к серверу
- Проверьте, что все зависимости установлены
- Сделайте резервную копию текущего состояния перед восстановлением

## 📞 Поддержка

При возникновении проблем обращайтесь к документации в папке `quantum-nexus/` или к файлу `RESTORE_INSTRUCTIONS.md`.

