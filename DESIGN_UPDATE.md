# Обновления дизайна Quantum Nexus

## Завершённые изменения

### 1. Кнопка тапа
- Добавлено неоновое свечение (`.tap-button::before` и `::after`)
- Анимация пульсации (2s infinite)
- Закруглённые края (border-radius: 50px)
- Убраны мерцания при нажатии

### 2. Заголовок
- Изменён с "⚛️ Quantum Nexus ⚛️" на "Quantum Nexus"
- Одна строка, без иконок
- Градиент и glow эффекты сохранены

### 3. Приветствие бота
- Переделано на описание с перспективами
- Кнопка "Открыть игру" открывает Web App автоматически
- Убрана информация о профиле из команды

### 4. API поддержки
- Добавлена модель `SupportTicket` в `models.py`
- API эндпоинт `/api/support` для создания тикетов
- API `/api/admin/support` для получения тикетов
- 10 категорий тем подготовлены

## Что нужно доделать вручную

### 1. Минификация главного экрана
В файле `web_app.html` найти секцию `.stats` и объединить отображение:

```html
<!-- Заменить текущий блок на: -->
<div class="stat-compact">
    <div class="stat-row">
        <div class="stat-item">
            <div class="stat-label">💰 Коины</div>
            <div class="stat-value">0</div>
            <div class="stat-passive">+0/час</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">💎 QuanHash</div>
            <div class="stat-value">0</div>
            <div class="stat-passive">+0/час</div>
        </div>
    </div>
</div>
```

### 2. Добавить CSS для компактной статистики

```css
.stat-compact {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(26, 29, 46, 0.95) 100%);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 15px;
    border: 1px solid rgba(102, 126, 234, 0.3);
}

.stat-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.stat-item {
    text-align: center;
    padding: 8px;
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
}

.stat-label {
    font-size: 11px;
    color: #94a3b8;
    margin-bottom: 4px;
}

.stat-value {
    font-size: 18px;
    font-weight: 900;
    color: #fff;
}

.stat-passive {
    font-size: 10px;
    color: #4ade80;
    margin-top: 2px;
}
```

### 3. Майнинг категории
Добавить в `web_server.py` обновлённый API для майнинга с категориями:

```python
@app.route('/api/mining', methods=['POST'])
def get_mining():
    """Get mining machines by category"""
    try:
        data = request.json
        user_id = data.get('user_id')
        category = data.get('category', 'starter')  # starter or premium
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if category == 'starter':
                # Machines for coins
                machines = [
                    {'id': 'basic', 'name': 'Базовая машина', 'price': 10000, 'hash_rate': 0.5, 'currency': 'coins'},
                    # ... еще 29 машин
                ]
            else:
                # Machines for QuanHash
                machines = [
                    {'id': 'premium_basic', 'name': 'Премиум Базовая', 'price': 500, 'hash_rate': 5.0, 'currency': 'quanhash'},
                    # ... еще 29 машин
                ]
            
            user_machines = db.query(MiningMachine).filter_by(user_id=user.id).all()
            
            return jsonify({
                'quanhash': user.quanhash,
                'category': category,
                'machines': machines,
                'user_machines': [{'id': m.id, 'type': m.machine_type, 'is_active': m.is_active} for m in user_machines]
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 4. Раздел поддержки в интерфейсе
Добавить в `web_app.html` модальное окно поддержки:

```html
<div id="supportModal" class="modal">
    <div class="modal-content">
        <h2>💬 Поддержка</h2>
        <select id="supportTopic" class="modal-input">
            <option>Общие вопросы</option>
            <option>Проблемы с балансом</option>
            <option>Вывод средств</option>
            <option>Майнинг</option>
            <option>Карточки</option>
            <option>Реферальная программа</option>
            <option>Технические проблемы</option>
            <option>Предложения</option>
            <option>Другое</option>
        </select>
        <textarea id="supportMessage" class="modal-input" placeholder="Опишите ваш вопрос..." rows="4"></textarea>
        <button onclick="sendSupport()">📤 Отправить</button>
        <button onclick="closeModal('supportModal')">Отмена</button>
    </div>
</div>
```

### 5. Магазин по категориям
Добавить категории в магазин (20 позиций на категорию):

```python
@app.route('/api/shop', methods=['POST'])
def get_shop():
    """Get shop items by category"""
    try:
        data = request.json
        category = data.get('category', 'boosts')  # boosts, energy, cards, auto
        
        categories = {
            'boosts': [
                {'id': 'multiplier_2x', 'name': '2x Множитель', 'price': 5000},
                # ... еще 19 позиций
            ],
            'energy': [
                {'id': 'energy_small', 'name': 'Энергия 100', 'price': 1000},
                # ... еще 19 позиций
            ],
            'cards': [
                {'id': 'common', 'name': 'Обычная карточка', 'price': 5000},
                # ... еще 19 позиций
            ],
            'auto': [
                {'id': 'auto_bot', 'name': 'Авто-бот', 'price': 50000},
                # ... еще 19 позиций
            ]
        }
        
        return jsonify({'category': category, 'items': categories.get(category, [])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 6. История транзакций
Добавить API для истории:

```python
@app.route('/api/history', methods=['POST'])
def get_history():
    """Get user transaction history"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            # Also get withdrawals
            withdrawals = db.query(Withdrawal).filter_by(user_id=user.id).all()
            
            history = []
            for t in user.transactions:
                history.append({
                    'type': t.transaction_type,
                    'amount': t.amount,
                    'currency': t.currency,
                    'date': t.created_at.isoformat() if t.created_at else None
                })
            
            for w in withdrawals:
                history.append({
                    'type': 'withdrawal',
                    'amount': w.usdt_amount,
                    'currency': 'usd',
                    'status': w.status,
                    'date': w.created_at.isoformat() if w.created_at else None
                })
            
            return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Инструкции по применению

1. Обновите сервер:
```bash
cd /root/quantum-nexus
git pull origin main
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
```

2. Инициализируйте новую таблицу:
```bash
sudo -u postgres psql -d quantum_nexus -c "ALTER TABLE users ADD COLUMN IF NOT EXISTS additional_field TEXT;"
```

3. Добавьте остальные изменения вручную согласно инструкциям выше.








