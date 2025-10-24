const express = require('express');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Static files
app.use(express.static('public'));

// Game data storage
const gameDataFile = 'gameData.json';
let gameData = {};

// Load game data
try {
  if (fs.existsSync(gameDataFile)) {
    const data = fs.readFileSync(gameDataFile, 'utf8');
    gameData = JSON.parse(data);
    console.log('Loaded game data:', gameData);
  } else {
    console.log('No game data file found, starting fresh');
  }
} catch (error) {
  console.log('Error loading game data:', error);
  gameData = {};
}

// Save game data
function saveGameData() {
  try {
    fs.writeFileSync(gameDataFile, JSON.stringify(gameData, null, 2));
    console.log('Saved game data:', gameData);
  } catch (error) {
    console.log('Error saving game data:', error);
  }
}

// API для игры
app.get('/api/game/:userId', (req, res) => {
  const userId = req.params.userId;
  if (!gameData[userId]) {
    gameData[userId] = {
      totalTaps: 0,
      energy: 100,
      coins: 0,
      level: 1,
      bitcoin: 0,
      multiplier: 1,
      maxEnergy: 100
    };
  }
  console.log('Getting game data for user:', userId, gameData[userId]);
  res.json({
    success: true,
    data: gameData[userId]
  });
});

app.post('/api/game/:userId/save', express.json(), (req, res) => {
  const userId = req.params.userId;
  gameData[userId] = req.body;
  console.log('Saving game data for user:', userId, req.body);
  saveGameData();
  res.json({ success: true });
});

// Главная страница
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Тестовая страница
app.get('/test', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Quantum Nexus Server is running!',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log('Quantum Nexus server running on port', PORT);
  console.log('Game available at: http://localhost:' + PORT);
  console.log('Test endpoint: http://localhost:' + PORT + '/test');
});
