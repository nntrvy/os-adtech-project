# Getting Started: 10-Minute Demo

**Goal**: See the full system working on your laptop in 10 minutes.

---

## Prerequisites

- Node.js 16+ installed
- Terminal access
- Web browser

---

## Step 1: Install & Run Backend (2 minutes)

```bash
cd /Users/nntrvy/os-adtech-project/taxi-mvp
npm install
npm start
```

You should see:
```
Server running on http://localhost:3000
Upload content at http://localhost:3000
Status API at http://localhost:3000/status
```

Leave this terminal running.

---

## Step 2: Open Admin Dashboard (1 minute)

1. Open browser: http://localhost:3000
2. You should see:
   - "Upload New Content" section
   - "Current Content" section (empty)
   - "Connected Devices" section (0 devices)

**This is your advertiser control panel.**

---

## Step 3: Simulate A Device (1 minute)

Open a NEW terminal:

```bash
cd /Users/nntrvy/os-adtech-project/taxi-mvp
node test-client.js
```

You should see:
```
Starting test client...
Simulating device: taxi_test_001
Server: http://localhost:3000
---
[2024-12-02T23:55:00.000Z] Heartbeat sent: 200
[2024-12-02T23:55:00.001Z] No content available
Client running. Press Ctrl+C to stop.
```

Leave this terminal running.

---

## Step 4: Verify Device Connected (1 minute)

1. Go back to browser: http://localhost:3000
2. Refresh page
3. You should now see:
   - "1 devices reporting"
   - "taxi_test_001 - Last seen: 0 min ago - Heartbeats: 1"

**The device is now "online"!**

---

## Step 5: Upload Content (2 minutes)

### Option A: Use a test image (easiest)

1. Download any JPEG image from internet
2. Save to your Downloads folder
3. In browser (http://localhost:3000):
   - Click "Choose File"
   - Select the JPEG
   - Click "Upload & Deploy"

### Option B: Create a test image

```bash
# Install ImageMagick (if not installed)
brew install imagemagick  # macOS

# Create simple ad image
convert -size 1920x1080 xc:blue \
  -pointsize 72 -fill white -gravity center \
  -annotate +0+0 'Test Ad\nNow Playing' \
  /tmp/test-ad.jpg

# Then upload via web UI
```

---

## Step 6: Watch Content Deploy (2 minutes)

After uploading, watch the test-client.js terminal:

Within 60 seconds, you'll see:
```
[2024-12-02T23:56:00.000Z] Content available: http://localhost:3000/uploads/1701563760000.jpg
```

**This simulates the taxi downloading your ad!**

---

## Step 7: Check Status API (1 minute)

Open a third terminal:

```bash
curl http://localhost:3000/status
```

You should see:
```json
{
  "total_devices_seen": 1,
  "online_now": 1,
  "heartbeats_last_hour": 2
}
```

**This is what monitoring systems would query.**

---

## What Just Happened?

```
You uploaded image
    ↓
Backend saved to /uploads/
    ↓
Backend marked as "active content"
    ↓
Device polled /content/taxi_test_001 (every 60s)
    ↓
Backend returned image URL
    ↓
Device "downloaded" and would display it
```

**This is EXACTLY how it works on real taxis.**

The only difference: real Android tablet would display the image fullscreen.

---

## Simulate Multiple Devices

Want to see 10 devices?

Open 10 terminals, each running:

```bash
# Terminal 1
DEVICE_ID=taxi_001 node test-client.js

# Terminal 2
DEVICE_ID=taxi_002 node test-client.js

# Terminal 3
DEVICE_ID=taxi_003 node test-client.js

# ... etc
```

Or create a simple script:

```bash
# /Users/nntrvy/os-adtech-project/taxi-mvp/simulate-fleet.sh
for i in {1..10}; do
  DEVICE_ID="taxi_$(printf %03d $i)" node test-client.js &
done
wait
```

Then run:
```bash
chmod +x simulate-fleet.sh
./simulate-fleet.sh
```

Refresh dashboard: you'll see 10 devices!

---

## Test Content Updates

1. Upload a new image
2. Watch all device terminals
3. Within 60s, they all log the new URL

**This proves content distribution works.**

---

## Inspect The Database

```bash
cd /Users/nntrvy/os-adtech-project/taxi-mvp
sqlite3 taxi.db
```

In SQLite shell:

```sql
-- See all content
SELECT * FROM content;

-- See recent heartbeats
SELECT * FROM heartbeats ORDER BY timestamp DESC LIMIT 10;

-- Count devices
SELECT COUNT(DISTINCT device_id) FROM heartbeats;

-- Exit
.quit
```

---

## Stop Everything

1. Close browser
2. Press Ctrl+C in all terminals
3. Database and uploads persist (in taxi-mvp/ folder)

To completely reset:

```bash
cd /Users/nntrvy/os-adtech-project/taxi-mvp
rm -rf taxi.db uploads/
npm start  # Fresh database
```

---

## Next Steps

### To Deploy This For Real:

1. **Deploy Backend**
   ```bash
   # Sign up for Railway (free tier)
   railway login
   railway init
   railway up

   # Note the public URL: https://your-app.railway.app
   ```

2. **Build Android App**
   - Use android-client.pseudo.kt as reference
   - Set SERVER_URL to your Railway URL
   - Build APK in Android Studio
   - Install on tablet

3. **Install Hardware**
   - See HARDWARE_SPEC.md for components
   - See DEPLOYMENT.md for installation guide
   - Configure each device with unique ID

4. **Monitor**
   - Check dashboard daily
   - Watch for devices going offline
   - Replace failed hardware

---

## Troubleshooting

### "Cannot find module 'express'"
```bash
cd /Users/nntrvy/os-adtech-project/taxi-mvp
rm -rf node_modules
npm install
```

### "EADDRINUSE: Port 3000 in use"
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm start
```

### "No content available" forever
1. Check server is running
2. Upload an image via dashboard
3. Wait up to 60s for device to poll

### Device not appearing in dashboard
1. Check test-client.js is running
2. Check no errors in terminal
3. Refresh browser (devices shown if heartbeat < 1 hour old)

---

## Understanding The Code

### Backend (server.js)

**Lines 1-50**: Database setup
- Create tables if not exist
- Set up indexes

**Lines 51-80**: Content endpoint
- Device polls GET /content/:device_id
- Returns active content URL

**Lines 81-100**: Heartbeat endpoint
- Device posts GPS location
- Logs to database

**Lines 101-200**: Web UI
- Shows upload form
- Lists active content
- Lists connected devices

**Lines 201-221**: Upload handler
- Saves file to disk
- Updates database
- Redirects to dashboard

**That's it. 221 lines total.**

### Device (test-client.js)

**Lines 1-30**: Heartbeat function
- Sends POST request with GPS
- Runs every 60s

**Lines 31-60**: Content check function
- Sends GET request
- Logs if new content available
- Runs every 60s

**Lines 61-84**: Main loop
- Starts both intervals
- Keeps running until Ctrl+C

**That's it. 84 lines total.**

---

## Key Metrics To Watch

### Device Health
- **Online now**: Should be ~95% of total fleet
- **Heartbeats last hour**: Should be ~devices × 60

Example: 50 devices × 60 heartbeats/hour = 3,000

### Content Distribution
- **Update latency**: Time from upload to device receipt
- Target: <5 minutes (most devices)

### Failures
- **Devices offline >1 hour**: Investigate
- **No heartbeats for device**: Hardware failure or theft

---

## Demo Script (For Investor Meeting)

**Minute 1-2**: Show Dashboard
- "This is our advertiser control panel"
- "Currently 50 taxis connected"
- Point to device list, show GPS locations

**Minute 3-5**: Upload Content
- "Let's deploy a new ad"
- Upload image
- "Content is now staged"

**Minute 6-8**: Show Live Update
- Open device terminal (or show Android tablet)
- "Watch: devices polling for updates"
- Show logs: "Content available"
- "All 50 taxis now showing the new ad"

**Minute 9-10**: Show Metrics
- curl /status endpoint
- "95% uptime over 30 days"
- "Average update time: 3 minutes"
- "Zero manual interventions"

**Conclusion**:
"We've proven we can remotely manage content on 50 moving vehicles. Technical feasibility validated. Ready to scale to 5,000."

---

## Common Questions

### Q: Why 60-second polling?
A: Balance between:
- Faster = more data usage + server load
- Slower = higher latency for updates
- 60s = sweet spot for MVP

### Q: What if device is offline when we push new content?
A: It gets the update when it comes back online (next poll).

### Q: How do we know if an ad is actually displaying?
A: MVP assumes if device is online, it's displaying. Phase 2 adds screenshot verification.

### Q: Can we target specific taxis?
A: Not in MVP (all get same content). Phase 2 adds geo-targeting.

### Q: What prevents someone else from polling our API?
A: Nothing in MVP. Phase 2 adds device authentication.

### Q: How do we handle video?
A: Not in MVP. Phase 2 extends to video files (same distribution mechanism).

---

## Success Criteria Reminder

After 30 days of operation, we should see:

✅ **80%+ uptime**: >40 of 50 devices reporting hourly
✅ **<10 min updates**: 90% of devices updated within 10 min
✅ **<5% hardware failures**: <3 devices replaced in 30 days
✅ **Zero manual interventions**: No need to physically visit taxis

**If we hit these numbers**: Technical feasibility validated, proceed to Phase 2.

**If we don't**: Analyze failures, determine if fixable or fundamental.

---

## Resources

- **Code**: /Users/nntrvy/os-adtech-project/taxi-mvp/
- **Docs**: Same folder, all .md files
- **Hardware guide**: HARDWARE_SPEC.md
- **Deployment plan**: DEPLOYMENT.md
- **Investor brief**: INVESTOR_BRIEF.md
- **Architecture**: ARCHITECTURE.md

---

**Now go build it. 4 weeks to validation.**
