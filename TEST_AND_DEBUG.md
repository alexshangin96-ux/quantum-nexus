# Тестирование Топ Лидеров

## Шаги для проверки:

1. **Проверьте, что бот работает:**
   ```bash
   sudo systemctl status quantum-nexus
   ```
   Должен показывать `active (running)`

2. **Откройте бота в Telegram и сделайте несколько тапов**

3. **Подождите 5-10 секунд**

4. **Откройте приложение и нажмите на иконку "Топ" (слева вверху)**

5. **Если топ пуст:**
   - Откройте DevTools в браузере (если возможно)
   - Посмотрите в Console на ошибки
   - Или проверьте логи web-сервера:
     ```bash
     sudo journalctl -u quantum-nexus-web -n 50 --no-pager
     ```

## Если ничего не помогает:

Проверьте, есть ли пользователи в базе данных:
```bash
cd /root/quantum-nexus
source venv/bin/activate
python3 -c "
from database import get_db
from models import User
with get_db() as db:
    users = db.query(User).all()
    print(f'Всего пользователей: {len(users)}')
    for u in users[:5]:
        print(f'{u.username}: total_earned={u.total_earned}, taps={u.total_taps}')
"
```

Если в базе нет пользователей или все `total_earned=0`, значит проблема в том, что:
1. Пользователи не взаимодействуют с ботом
2. Или `total_earned` не обновляется
