// Quantum Nexus - God Admin Panel Script

const ADMIN_LOGIN = 'smartfixnsk';
const ADMIN_PASSWORD = 'Maga1996';

let quickEditData = null;

// Create particles
function createParticles() {
    const container = document.getElementById('particles');
    for (let i = 0; i < 100; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (15 + Math.random() * 25) + 's';
        container.appendChild(particle);
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    const text = document.getElementById('notification-text');
    notification.classList.remove('hidden', 'success', 'error', 'info');
    notification.classList.add(type);
    text.textContent = message;
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 4000);
}

// Quick edit modal
function openQuickEdit(userId, field, title) {
    quickEditData = { userId, field };
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalInput').value = '';
    document.getElementById('quickEditModal').classList.add('active');
}

function closeModal() {
    document.getElementById('quickEditModal').classList.remove('active');
    quickEditData = null;
}

function confirmQuickEdit() {
    if (!quickEditData) return;
    const value = parseFloat(document.getElementById('modalInput').value);
    if (isNaN(value)) {
        showNotification('❌ Введите корректное значение', 'error');
        return;
    }
    
    modifyUser(quickEditData.userId, `set_${quickEditData.field}`, value);
    closeModal();
}

// Auto-login check
window.addEventListener('load', () => {
    createParticles();
    if (localStorage.getItem('admin_logged_in') === 'true') {
        initPanel();
    }
});

function login() {
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    if (login === ADMIN_LOGIN && password === ADMIN_PASSWORD) {
        localStorage.setItem('admin_logged_in', 'true');
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('adminPanel').classList.remove('hidden');
        initPanel();
        showNotification('✅ Авторизация успешна', 'success');
    } else {
        showNotification('❌ Неверный логин или пароль', 'error');
    }
}

function logout() {
    localStorage.removeItem('admin_logged_in');
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('adminPanel').classList.add('hidden');
    showNotification('👋 Выход выполнен', 'info');
}

function initPanel() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('adminPanel').classList.remove('hidden');
    loadDashboard();
    loadUsers();
}

function loadDashboard() {
    fetch('/api/admin/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalUsers').textContent = formatNumber(data.total_users || 0);
            document.getElementById('totalRevenue').textContent = formatNumber(data.total_revenue || 0);
            document.getElementById('totalActivity').textContent = formatNumber(data.active_users || 0);
            document.getElementById('totalWithdrawals').textContent = formatNumber(data.pending_withdrawals || 0);
            document.getElementById('totalTaps').textContent = formatNumber(data.total_taps || 0);
            document.getElementById('totalReferrals').textContent = formatNumber(data.total_referrals || 0);
        })
        .catch(err => console.error('Error loading dashboard:', err));
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    loadTab(tabName);
}

function loadTab(tabName) {
    const content = document.getElementById('content');
    
    if (tabName === 'users') {
        loadUsers();
    } else if (tabName === 'withdrawals') {
        loadWithdrawals();
    } else if (tabName === 'stats') {
        loadStats();
    } else if (tabName === 'logs') {
        loadLogs();
    } else if (tabName === 'settings') {
        loadSettings();
    }
}

function loadUsers() {
    const content = document.getElementById('content');
    content.innerHTML = '<div class="loading">Загрузка пользователей...</div>';
    
    fetch('/api/admin/users')
        .then(res => res.json())
        .then(data => {
            if (data.users && data.users.length > 0) {
                window.allUsers = data.users;
                renderUsers(data.users);
                showNotification(`✅ Загружено ${data.users.length} пользователей`, 'success');
            } else {
                content.innerHTML = '<div class="empty-state"><div class="empty-state-icon">👥</div><p>Нет пользователей</p></div>';
            }
        })
        .catch(err => {
            content.innerHTML = '<div class="empty-state" style="color: #ef4444;"><div class="empty-state-icon">❌</div><p>Ошибка загрузки</p></div>';
            showNotification('❌ Ошибка загрузки пользователей', 'error');
        });
}

function renderUsers(users) {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="search-container">
            <input type="text" class="search-input" id="searchInput" placeholder="🔍 Поиск по имени или ID..." onkeyup="filterUsers()">
        </div>
        <div class="users-grid" id="usersList">
            ${users.map(user => createUserCard(user)).join('')}
        </div>
    `;
}

function createUserCard(user) {
    return `
        <div class="user-card" data-id="${user.telegram_id}" data-username="${user.username || ''}">
            <div class="user-header">
                <div class="user-info">
                    <h3>${user.username || 'Unknown'}</h3>
                    <div class="user-id">ID: ${user.telegram_id}</div>
                </div>
                <div class="user-badges">
                    ${user.is_banned ? '<span class="badge badge-banned">🔒 Заблокирован</span>' : ''}
                    ${user.is_frozen ? '<span class="badge badge-frozen">❄️ Заморожен</span>' : ''}
                </div>
            </div>
            <div class="stats-grid-mini">
                <div class="stat-item">
                    <div class="stat-label-small">💰 Коины</div>
                    <div class="stat-value-small">${formatNumber(user.coins)}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label-small">💎 QuanHash</div>
                    <div class="stat-value-small">${formatNumber(user.quanhash)}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label-small">⚡ Энергия</div>
                    <div class="stat-value-small">${user.energy}/${user.max_energy}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label-small">👆 Тапов</div>
                    <div class="stat-value-small">${formatNumber(user.total_taps)}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label-small">💵 Заработано</div>
                    <div class="stat-value-small">${formatNumber(user.total_earned)}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label-small">👥 Рефералов</div>
                    <div class="stat-value-small">${user.referrals_count}</div>
                </div>
            </div>
            <div class="actions-grid">
                <button class="action-btn btn-add" onclick="quickEdit(${user.telegram_id}, 'coins', '💰 Коины')">💰 Коины</button>
                <button class="action-btn btn-add" onclick="quickEdit(${user.telegram_id}, 'quanhash', '💎 QuanHash')">💎 QuanHash</button>
                <button class="action-btn btn-add" onclick="modifyUser(${user.telegram_id}, 'add_coins', 10000)">+10k 🪙</button>
                <button class="action-btn btn-add" onclick="modifyUser(${user.telegram_id}, 'add_coins', 100000)">+100k 🪙</button>
                <button class="action-btn btn-add" onclick="modifyUser(${user.telegram_id}, 'add_quanhash', 10000)">+10k 💎</button>
                <button class="action-btn btn-add" onclick="modifyUser(${user.telegram_id}, 'add_quanhash', 100000)">+100k 💎</button>
                <button class="action-btn btn-remove" onclick="modifyUser(${user.telegram_id}, 'remove_coins', 5000)">-5k 🪙</button>
                <button class="action-btn btn-status" onclick="setEnergy(${user.telegram_id}, ${user.max_energy})">⚡ Полная</button>
                ${user.is_banned ? 
                    '<button class="action-btn btn-success" onclick="modifyUser(' + user.telegram_id + ', \'unban\', \'\')">🔓 Разблокировать</button>' :
                    '<button class="action-btn btn-status" onclick="modifyUser(' + user.telegram_id + ', \'ban\', \'Admin ban\')">🔒 Заблокировать</button>'
                }
                ${user.is_frozen ? 
                    '<button class="action-btn btn-success" onclick="modifyUser(' + user.telegram_id + ', \'unfreeze\', \'\')">🔥 Разморозить</button>' :
                    '<button class="action-btn btn-status" onclick="modifyUser(' + user.telegram_id + ', \'freeze\', \'\')">❄️ Заморозить</button>'
                }
            </div>
            <button class="action-btn btn-reset" onclick="modifyUser(${user.telegram_id}, 'reset', 0)">⚠️ Сбросить аккаунт</button>
        </div>
    `;
}

function quickEdit(userId, field, title) {
    openQuickEdit(userId, field, title);
}

function filterUsers() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const filtered = window.allUsers.filter(u => 
        (u.username && u.username.toLowerCase().includes(search)) ||
        u.telegram_id.toString().includes(search)
    );
    document.getElementById('usersList').innerHTML = filtered.map(user => createUserCard(user)).join('');
}

function modifyUser(userId, action, value) {
    fetch('/api/admin/modify_user', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id: userId, action: action, value: value})
    })
    .then(() => {
        showNotification('✅ Изменения применены', 'success');
        loadUsers();
    })
    .catch(err => showNotification('❌ Ошибка: ' + err, 'error'));
}

function setEnergy(userId, maxEnergy) {
    fetch('/api/admin/set_energy', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id: userId, energy: maxEnergy})
    })
    .then(() => {
        showNotification('⚡ Энергия восстановлена', 'success');
        loadUsers();
    });
}

function loadWithdrawals() {
    const content = document.getElementById('content');
    content.innerHTML = '<div class="loading">Загрузка заявок...</div>';
    
    fetch('/api/admin/withdrawals')
        .then(res => res.json())
        .then(data => {
            if (data.requests && data.requests.length > 0) {
                content.innerHTML = data.requests.map(req => `
                    <div class="user-card">
                        <h3 style="margin-bottom: 20px; font-size: 28px;">Заявка #${req.id}</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div><strong>User ID:</strong> ${req.user_id}</div>
                            <div><strong>QuanHash:</strong> ${formatNumber(req.amount)}</div>
                            <div><strong>USDT:</strong> $${req.usdt_amount}</div>
                            <div><strong>Статус:</strong> ${req.status}</div>
                        </div>
                        <div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; font-family: monospace; word-break: break-all; color: #4ade80;">
                            ${req.address}
                        </div>
                        ${req.status === 'pending' ? `
                            <div style="display: flex; gap: 12px; margin-top: 20px;">
                                <button class="action-btn btn-success" style="flex: 1; padding: 18px;" onclick="processWithdrawal(${req.id}, 'completed')">✅ Одобрить</button>
                                <button class="action-btn btn-remove" style="flex: 1; padding: 18px;" onclick="processWithdrawal(${req.id}, 'rejected')">❌ Отклонить</button>
                            </div>
                        ` : ''}
                    </div>
                `).join('');
            } else {
                content.innerHTML = '<div class="empty-state"><div class="empty-state-icon">💸</div><p>Нет заявок на вывод</p></div>';
            }
        });
}

function processWithdrawal(requestId, status) {
    fetch('/api/admin/process_withdrawal', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({request_id: requestId, status: status})
    })
    .then(() => {
        showNotification(status === 'completed' ? '✅ Заявка одобрена' : '❌ Заявка отклонена', status === 'completed' ? 'success' : 'error');
        loadWithdrawals();
    });
}

function loadStats() {
    const content = document.getElementById('content');
    fetch('/api/admin/stats')
        .then(res => res.json())
        .then(data => {
            content.innerHTML = `
                <div style="display: grid; gap: 32px;">
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px;">
                        <div class="stat-card">
                            <span class="stat-icon">👥</span>
                            <div class="stat-label">Пользователей</div>
                            <div class="stat-value">${formatNumber(data.total_users || 0)}</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-icon">👆</span>
                            <div class="stat-label">Всего тапов</div>
                            <div class="stat-value">${formatNumber(data.total_taps || 0)}</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-icon">💸</span>
                            <div class="stat-label">Заявок</div>
                            <div class="stat-value">${formatNumber(data.pending_withdrawals || 0)}</div>
                        </div>
                    </div>
                </div>
            `;
        });
}

function loadLogs() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">📝</div>
            <p>Система логов в разработке</p>
            <p style="margin-top: 20px; opacity: 0.5;">Скоро будут доступны детальные логи всех действий</p>
        </div>
    `;
}

function loadSettings() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">⚙️</div>
            <p>Панель настроек скоро</p>
            <p style="margin-top: 20px; opacity: 0.5;">Настройки игры будут доступны здесь</p>
        </div>
    `;
}

function refreshAll() {
    loadDashboard();
    loadUsers();
    showNotification('🔄 Данные обновлены', 'success');
}

function formatNumber(num) {
    return Math.floor(num || 0).toLocaleString('ru');
}

document.getElementById('password')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') login();
});





