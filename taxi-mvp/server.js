const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();

// Simple JSON file storage
const DATA_DIR = './data';
const HEARTBEATS_FILE = path.join(DATA_DIR, 'heartbeats.json');
const CONTENT_FILE = path.join(DATA_DIR, 'content.json');

// Initialize data storage
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR);
}

function loadJSON(file, defaultValue = []) {
  try {
    if (fs.existsSync(file)) {
      return JSON.parse(fs.readFileSync(file, 'utf8'));
    }
  } catch (e) {}
  return defaultValue;
}

function saveJSON(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

// Middleware
app.use(express.json());
app.use('/uploads', express.static('uploads'));

// Ensure uploads directory exists
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

// Configure multer for image uploads
const storage = multer.diskStorage({
  destination: 'uploads/',
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});
const upload = multer({ storage });

// Device polls this endpoint to get current content
app.get('/content/:device_id', (req, res) => {
  const { device_id } = req.params;

  // Get active content
  const content = loadJSON(CONTENT_FILE);
  const activeContent = content.find(c => c.active === 1);

  if (!activeContent) {
    return res.json({ images: [] });
  }

  // Return full URL for the image
  const baseUrl = process.env.BASE_URL || `http://localhost:${PORT}`;
  res.json({
    images: [`${baseUrl}${activeContent.image_url}`]
  });
});

// Device sends heartbeat
app.post('/heartbeat', (req, res) => {
  const { device_id, latitude, longitude } = req.body;

  if (!device_id) {
    return res.status(400).json({ error: 'device_id required' });
  }

  const heartbeats = loadJSON(HEARTBEATS_FILE);
  heartbeats.push({
    device_id,
    latitude: latitude || null,
    longitude: longitude || null,
    timestamp: Date.now()
  });

  // Keep only last 1000 heartbeats to prevent file bloat
  if (heartbeats.length > 1000) {
    heartbeats.splice(0, heartbeats.length - 1000);
  }

  saveJSON(HEARTBEATS_FILE, heartbeats);
  res.json({ success: true });
});

// Web UI: Upload new content
app.get('/', (req, res) => {
  const content = loadJSON(CONTENT_FILE);
  const activeContent = content.filter(c => c.active === 1);

  const heartbeats = loadJSON(HEARTBEATS_FILE);
  const oneHourAgo = Date.now() - 3600000;

  // Group heartbeats by device
  const deviceMap = {};
  heartbeats
    .filter(h => h.timestamp > oneHourAgo)
    .forEach(h => {
      if (!deviceMap[h.device_id]) {
        deviceMap[h.device_id] = {
          device_id: h.device_id,
          last_seen: h.timestamp,
          heartbeat_count: 0
        };
      }
      deviceMap[h.device_id].last_seen = Math.max(deviceMap[h.device_id].last_seen, h.timestamp);
      deviceMap[h.device_id].heartbeat_count++;
    });

  const devices = Object.values(deviceMap).sort((a, b) => b.last_seen - a.last_seen);

  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Taxi DOOH Control</title>
      <meta http-equiv="refresh" content="5">
      <style>
        body { font-family: sans-serif; max-width: 1200px; margin: 50px auto; padding: 20px; background: #f8f9fa; }
        h1 { color: #333; }
        .section { margin: 40px 0; padding: 20px; border: 1px solid #ddd; background: white; border-radius: 8px; }
        .device { padding: 10px; margin: 5px 0; background: #f5f5f5; border-radius: 4px; }
        .online { border-left: 4px solid #4CAF50; }
        .offline { border-left: 4px solid #f44336; }
        img { max-width: 300px; margin: 10px 0; border: 1px solid #ddd; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; border-radius: 4px; font-size: 16px; }
        button:hover { background: #45a049; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat { padding: 20px; background: #e3f2fd; border-radius: 8px; flex: 1; text-align: center; }
        .stat h3 { margin: 0; font-size: 36px; color: #1976d2; }
        .stat p { margin: 5px 0 0 0; color: #666; }
      </style>
    </head>
    <body>
      <h1>🚕 Taxi DOOH MVP Control Dashboard</h1>

      <div class="stats">
        <div class="stat">
          <h3>${devices.length}</h3>
          <p>Active Devices</p>
        </div>
        <div class="stat">
          <h3>${devices.filter(d => (Date.now() - d.last_seen) < 300000).length}</h3>
          <p>Online Now</p>
        </div>
        <div class="stat">
          <h3>${activeContent.length > 0 ? '✓' : '✗'}</h3>
          <p>Content Deployed</p>
        </div>
      </div>

      <div class="section">
        <h2>📤 Upload New Content</h2>
        <form action="/upload" method="POST" enctype="multipart/form-data">
          <input type="file" name="image" accept="image/jpeg,image/png" required>
          <button type="submit">Upload & Deploy to All Taxis</button>
        </form>
        <p style="color: #666; font-size: 14px; margin-top: 10px;">
          Uploads a new ad and automatically deploys to all ${devices.length} connected taxis within 60 seconds.
        </p>
      </div>

      <div class="section">
        <h2>📺 Current Content</h2>
        ${activeContent.length === 0 ? '<p>No active content deployed</p>' :
          activeContent.map(c => `
            <div>
              <img src="${c.image_url}" alt="Current ad">
              <p><strong>Deployed:</strong> ${new Date(c.created_at).toLocaleString()}</p>
              <p><strong>Status:</strong> <span style="color: #4CAF50;">● LIVE on ${devices.filter(d => (Date.now() - d.last_seen) < 300000).length} taxis</span></p>
            </div>
          `).join('')
        }
      </div>

      <div class="section">
        <h2>🚖 Connected Devices (Last Hour)</h2>
        <p><strong>${devices.length}</strong> taxi${devices.length !== 1 ? 's' : ''} reporting</p>
        ${devices.length === 0 ? '<p style="color: #999;">No devices connected yet. Run test-client.js to simulate taxis.</p>' :
          devices.map(d => {
            const minutesAgo = Math.floor((Date.now() - d.last_seen) / 60000);
            const isOnline = minutesAgo < 5;
            return `
              <div class="device ${isOnline ? 'online' : 'offline'}">
                <strong>Taxi ${d.device_id}</strong> -
                Last seen: ${minutesAgo < 1 ? 'just now' : minutesAgo + ' min ago'} -
                Heartbeats: ${d.heartbeat_count}
              </div>
            `;
          }).join('')}
      </div>

      <div style="margin-top: 40px; padding: 20px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107;">
        <h3 style="margin-top: 0;">🎯 MVP Validation Goals:</h3>
        <ul>
          <li><strong>80%+ uptime</strong>: Devices report heartbeat every minute</li>
          <li><strong>&lt;10 min updates</strong>: Content reaches 90% of fleet within 10 minutes</li>
          <li><strong>&lt;5% hardware failures</strong>: Over 30 days of operation</li>
          <li><strong>Zero manual interventions</strong>: No physical taxi access needed</li>
        </ul>
        <p style="margin-bottom: 0;"><em>Page auto-refreshes every 5 seconds</em></p>
      </div>
    </body>
    </html>
  `);
});

// Handle image upload
app.post('/upload', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded');
  }

  // Deactivate old content
  const content = loadJSON(CONTENT_FILE);
  content.forEach(c => c.active = 0);

  // Insert new content
  const imageUrl = `/uploads/${req.file.filename}`;
  content.push({
    id: content.length + 1,
    image_url: imageUrl,
    active: 1,
    created_at: Date.now()
  });

  saveJSON(CONTENT_FILE, content);
  res.redirect('/');
});

// Device status endpoint
app.get('/status', (req, res) => {
  const heartbeats = loadJSON(HEARTBEATS_FILE);

  const uniqueDevices = new Set(heartbeats.map(h => h.device_id));
  const fiveMinAgo = Date.now() - 300000;
  const oneHourAgo = Date.now() - 3600000;

  const onlineDevices = new Set(
    heartbeats
      .filter(h => h.timestamp > fiveMinAgo)
      .map(h => h.device_id)
  );

  const lastHourHeartbeats = heartbeats.filter(h => h.timestamp > oneHourAgo).length;

  res.json({
    total_devices_seen: uniqueDevices.size,
    online_now: onlineDevices.size,
    heartbeats_last_hour: lastHourHeartbeats,
    uptime_percentage: uniqueDevices.size > 0 ? ((onlineDevices.size / uniqueDevices.size) * 100).toFixed(1) : 0
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('\n🚕 Taxi DOOH MVP Server Started!');
  console.log('================================');
  console.log(`📊 Dashboard: http://localhost:${PORT}`);
  console.log(`📡 Status API: http://localhost:${PORT}/status`);
  console.log(`📱 Device API: http://localhost:${PORT}/content/:device_id`);
  console.log('\n💡 Next steps:');
  console.log('   1. Open the dashboard in your browser');
  console.log('   2. Run "node test-client.js" to simulate taxis');
  console.log('   3. Upload an image to see it deployed\n');
});
