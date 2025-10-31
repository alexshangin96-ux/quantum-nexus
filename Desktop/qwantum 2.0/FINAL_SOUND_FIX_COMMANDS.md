# 🔊 Финальные команды для обновления звука на Selectel

## ⚠️ Важно: Сейчас работают ВСЕ логи для отладки!
Логи покажут точную причину проблем со звуком в консоли браузера/DevTools.

## 🚀 БЫСТРАЯ КОМАНДА (копируйте всю строку):

```bash
cd /root/quantum-nexus && git pull origin main && sudo cp web_app.html /var/www/quantum-nexus/web_app.html && sudo systemctl restart quantum-nexus-web.service
```

---

## 📋 Пошаговые команды:

### 1. Подключитесь к серверу:
```bash
ssh root@your-server-ip
```

### 2. Перейдите в папку проекта:
```bash
cd /root/quantum-nexus
```

### 3. Обновите код:
```bash
git pull origin main
```

### 4. Скопируйте обновленный файл:
```bash
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
```

### 5. Перезапустите веб-сервис:
```bash
sudo systemctl restart quantum-nexus-web.service
```

### 6. Проверьте статус:
```bash
sudo systemctl status quantum-nexus-web.service
```

---

## ✅ Проверка работы звука:

### После обновления:
1. Откройте приложение в Telegram
2. Зайдите в **Настройки ⚙️**
3. Убедитесь, что переключатель **Звуки** выключен (серый)
4. Включите **Звуки** (переключатель станет синим)
5. Нажмите **Сохранить**
6. Попробуйте сделать тап

### Что должно произойти:
- ✅ При включении звука и сохранении настроек должен прозвучать звук `success`
- ✅ При тапе должен прозвучать звук `tap`
- ✅ Вибрация работает в любом случае, если включена

---

## 🐛 Отладка звука в браузере:

### Откройте консоль разработчика:

**В Telegram WebView:**
1. Используйте DevTools или удаленную отладку
2. Откройте Console

### Что смотреть в логах:

#### 1. При переключении звука:
```
Sound toggle changed: true
```
или
```
Sound toggle changed: false
```

#### 2. При сохранении настроек:
```
saveSettings - soundEnabled: true hapticsEnabled: true
Saved soundEnabled to localStorage: true
About to play success sound, soundEnabled === true? true
Playing success sound after settings save
```

#### 3. При попытке воспроизвести звук:
```
Playing sound: success
AudioContext created, state: suspended
AudioContext suspended, attempting to resume...
AudioContext resumed successfully, state: running
Creating oscillator for sound: success AudioContext: {...}
Oscillator created: {...}
Gain node created: {...}
Oscillator connected to gain
Gain connected to destination: {...}
Gain envelope set
Sound started successfully: success
```

### Если звук НЕ работает, проверьте логи:

#### Проблема 1: Звук отключен
```
Sound disabled, setting: null
```
или
```
Sound disabled, setting: false
```
**Решение:** Включите звук в настройках!

#### Проблема 2: AudioContext не создается
```
Audio not supported: [ошибка]
```
**Решение:** Проблема с браузером/платформой

#### Проблема 3: AudioContext suspended и не возобновляется
```
AudioContext suspended, attempting to resume...
AudioContext resumed successfully, state: running
```
Но звука все равно нет.

**Решение:** Возможно нужен user gesture. Попробуйте кликнуть по элементу вручную.

#### Проблема 4: Ошибка при создании oscillator
```
Creating oscillator for sound: tap AudioContext: {...}
```
И НЕТ дальнейших логов.

**Решение:** AudioContext поврежден или не поддерживается

---

## 🔧 Проверка состояния вручную:

### В консоли браузера выполните:

```javascript
// Проверьте значение в localStorage
localStorage.getItem('soundEnabled')  
// Должно быть 'true' или 'false'

// Проверьте состояние AudioContext
window.audioContext?.state  
// Должно быть 'running' или 'suspended'

// Создайте AudioContext вручную
const ctx = new AudioContext();
console.log('Manual context state:', ctx.state);
```

---

## 📊 История изменений:

### Коммит 5a46aac:
- Звук и вибрация по умолчанию выключены
- Исправлена логика проверки: `=== 'true'`

### Коммит 667e14a:
- Добавлено логирование в playSound
- Исправлены проверки в saveSettings

### Коммит 45d8f6b:
- Добавлено логирование при переключении звука
- Добавлено логирование состояния AudioContext

### Коммит e017b25:
- Добавлено детальное логирование создания oscillator и gain node
- Показывает каждый шаг воспроизведения звука

---

## 🆘 Если ничего не работает:

1. Проверьте логи на сервере:
   ```bash
   sudo journalctl -u quantum-nexus-web.service -n 100
   ```

2. Посмотрите последние коммиты:
   ```bash
   git log --oneline -5
   ```

3. Откатитесь к предыдущей версии:
   ```bash
   git reset --hard HEAD~1
   git push --force origin main
   sudo cp web_app.html /var/www/quantum-nexus/web_app.html
   sudo systemctl restart quantum-nexus-web.service
   ```

4. Создайте issue на GitHub с логами из консоли браузера

---

## 📝 После успешной отладки:

Когда звук заработает, **УДАЛИТЕ ЛОГИ** для продакшена (они замедляют работу):

Удалите все `console.log` из:
- `initAudio()`
- `playSound()`
- `saveSettings()`
- checkbox `onchange` в настройках

И сделайте финальный коммит без логов.

