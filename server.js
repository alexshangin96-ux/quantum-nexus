const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Static files
app.use(express.static('public'));

// Game API
app.get('/api/game/:userId', (req, res) => {
  res.json({
    success: true,
    data: {
      totalTaps: 0,
      energy: 100,
      coins: 0,
      level: 1,
      bitcoin: 0,
      multiplier: 1
    }
  });
});

app.post('/api/game/:userId/save', express.json(), (req, res) => {
  console.log('Saving player data:', req.params.userId);
  res.json({ success: true });
});

// Main page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Test page
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
