// Simple test client that simulates an Android device
// Run this to test the backend without actual hardware

const http = require('http');

const SERVER_URL = 'http://localhost:3000';
const DEVICE_ID = 'taxi_test_001';

function sendHeartbeat() {
  const data = JSON.stringify({
    device_id: DEVICE_ID,
    latitude: 10.762622 + (Math.random() - 0.5) * 0.01, // Simulate movement around HCMC
    longitude: 106.660172 + (Math.random() - 0.5) * 0.01
  });

  const options = {
    hostname: 'localhost',
    port: 3000,
    path: '/heartbeat',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length
    }
  };

  const req = http.request(options, (res) => {
    console.log(`[${new Date().toISOString()}] Heartbeat sent: ${res.statusCode}`);
  });

  req.on('error', (e) => {
    console.error(`Error: ${e.message}`);
  });

  req.write(data);
  req.end();
}

function checkContent() {
  const options = {
    hostname: 'localhost',
    port: 3000,
    path: `/content/${DEVICE_ID}`,
    method: 'GET'
  };

  const req = http.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      const response = JSON.parse(data);
      if (response.images && response.images.length > 0) {
        console.log(`[${new Date().toISOString()}] Content available: ${response.images[0]}`);
      } else {
        console.log(`[${new Date().toISOString()}] No content available`);
      }
    });
  });

  req.on('error', (e) => {
    console.error(`Error: ${e.message}`);
  });

  req.end();
}

console.log('Starting test client...');
console.log(`Simulating device: ${DEVICE_ID}`);
console.log(`Server: ${SERVER_URL}`);
console.log('---');

// Send heartbeat every 60 seconds
setInterval(sendHeartbeat, 60000);
sendHeartbeat(); // Send immediately

// Check for content every 60 seconds
setInterval(checkContent, 60000);
checkContent(); // Check immediately

console.log('Client running. Press Ctrl+C to stop.');
