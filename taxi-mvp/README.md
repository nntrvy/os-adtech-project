# Taxi DOOH Feasibility MVP

Single-feature MVP to validate: **Can we remotely distribute content to 50,000 taxi screens?**

## What This Does

- Upload JPEG images via web UI
- Push content to taxi devices via 4G
- Receive heartbeat signals from devices
- Monitor device online/offline status

## What This Does NOT Do

- Video playback (images only)
- Programmatic bidding (manual uploads)
- Analytics (raw logs only)
- Authentication (single user)
- Ad scheduling (instant deploy)

## Tech Stack

- **Backend**: Node.js + Express + SQLite
- **Device**: Android tablet polling server every 60s
- **Storage**: Local filesystem (upgrade to S3 later)
- **Connectivity**: 4G SIM cards in tablets

## Quick Start

```bash
npm install
npm start
```

Open http://localhost:3000 to:
- Upload new ad creative
- See current deployed content
- Monitor connected devices

## API Endpoints

### Device Endpoints (called by Android app)

**GET /content/:device_id**
- Returns current active content URLs
- Polled every 60 seconds by device

**POST /heartbeat**
```json
{
  "device_id": "taxi_001",
  "latitude": 10.762622,
  "longitude": 106.660172
}
```

### Web UI

**GET /**
- Upload form + device status dashboard

**GET /status**
- JSON summary of device fleet health

## Device Setup

1. Install Android APK on tablet
2. Configure device_id (e.g., "taxi_001")
3. Set server URL in app config
4. Insert 4G SIM card
5. Mount to taxi roof with power connection

## Success Metrics (30 Days)

- ✅ 80%+ devices report heartbeat hourly
- ✅ <10 min content update time
- ✅ <5% hardware failure rate
- ✅ Zero manual interventions required

## Deployment

Deploy to Railway/Render:
1. Push to Git
2. Set environment variable: `BASE_URL=https://your-domain.com`
3. Deploy

## Next Steps (After Validation)

If we hit success metrics with 50 taxis:
- Build proper CDN integration
- Add video playback
- Create advertiser dashboard
- Implement geo-targeting
- Add viewability tracking
- Build programmatic bidding system

**But NOT before we prove the hardware/connectivity works.**
