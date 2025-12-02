# System Architecture: Taxi DOOH MVP

## High-Level Overview

```
┌─────────────────┐
│   Advertiser    │
│  (Web Browser)  │
└────────┬────────┘
         │
         │ 1. Upload JPEG image
         ▼
┌─────────────────────────────┐
│   Backend Server            │
│   (Node.js + SQLite)        │
│   - Stores content          │
│   - Logs heartbeats         │
│   - Serves API              │
└────────┬────────────────────┘
         │
         │ 2. Poll every 60s
         │ 3. Download image URL
         ▼
┌─────────────────────────────┐
│   Taxi Device (x50)         │
│   - Android tablet          │
│   - 4G connection           │
│   - Displays fullscreen ad  │
└─────────────────────────────┘
```

---

## Data Flow

### Content Distribution

```
1. Advertiser uploads image
   POST /upload
   ↓
2. Server saves to /uploads/
   ↓
3. Server marks content as active in SQLite
   ↓
4. Device polls: GET /content/:device_id
   ↓
5. Server returns image URL
   ↓
6. Device downloads and displays image
```

**Latency**: 0-60 seconds (depends on when device next polls)

### Heartbeat Monitoring

```
1. Device collects GPS location
   ↓
2. Device sends: POST /heartbeat
   { device_id, latitude, longitude }
   ↓
3. Server logs to SQLite with timestamp
   ↓
4. Admin dashboard queries recent heartbeats
   ↓
5. Shows which devices are online/offline
```

**Frequency**: Every 60 seconds per device

---

## Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        Backend Server                         │
│                     (Railway/Render - $5/mo)                  │
│                                                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │   Web UI       │  │   API Routes   │  │   Database     │ │
│  │                │  │                │  │                │ │
│  │  - Upload form │  │  GET /content  │  │  SQLite:       │ │
│  │  - Device list │  │  POST /beat    │  │  - content     │ │
│  │  - Status view │  │  GET /status   │  │  - heartbeats  │ │
│  └────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Static Files: /uploads/                   │  │
│  │              (JPEG images served via HTTP)             │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                                 ▲
                                 │
                        HTTP over Internet
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                      Taxi Device (x50)                        │
│                                                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │  Android OS    │  │  4G Modem      │  │  GPS Module    │ │
│  │  (10" tablet)  │  │  (SIM card)    │  │  (built-in)    │ │
│  └────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Custom App (APK)                          │  │
│  │                                                         │  │
│  │  - Polls server every 60s                              │  │
│  │  - Downloads images to cache                           │  │
│  │  - Displays fullscreen                                 │  │
│  │  - Sends GPS heartbeat                                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌────────────────┐                                           │
│  │  Power Supply  │  (12V car battery → 5V USB)              │
│  └────────────────┘                                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Database Schema

### Table: `content`
```sql
CREATE TABLE content (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  image_url TEXT NOT NULL,           -- e.g., "/uploads/1701234567890.jpg"
  active INTEGER DEFAULT 1,          -- 1 = active, 0 = archived
  created_at INTEGER NOT NULL        -- Unix timestamp
);
```

**Purpose**: Store uploaded ad creatives
**Size**: ~10 rows (1 active, 9 archived)

### Table: `heartbeats`
```sql
CREATE TABLE heartbeats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id TEXT NOT NULL,           -- e.g., "taxi_001"
  latitude REAL,                     -- GPS coordinate
  longitude REAL,                    -- GPS coordinate
  timestamp INTEGER NOT NULL         -- Unix timestamp
);

CREATE INDEX idx_device_timestamp ON heartbeats(device_id, timestamp);
```

**Purpose**: Log device connectivity and location
**Size**: ~72,000 rows/day (50 devices × 1 heartbeat/min × 1,440 min/day)
**Growth**: ~2M rows/month

**Note**: For MVP, this is fine. For production, add cleanup job to delete rows older than 30 days.

---

## API Specification

### GET /content/:device_id

**Called by**: Device (every 60 seconds)

**Request**:
```
GET /content/taxi_001 HTTP/1.1
Host: your-backend.com
```

**Response**:
```json
{
  "images": [
    "https://your-backend.com/uploads/1701234567890.jpg"
  ]
}
```

**Edge cases**:
- No active content: `{"images": []}`
- Invalid device_id: Still returns content (no per-device targeting in MVP)

---

### POST /heartbeat

**Called by**: Device (every 60 seconds)

**Request**:
```
POST /heartbeat HTTP/1.1
Host: your-backend.com
Content-Type: application/json

{
  "device_id": "taxi_001",
  "latitude": 10.762622,
  "longitude": 106.660172
}
```

**Response**:
```json
{
  "success": true
}
```

**Edge cases**:
- Missing device_id: `400 Bad Request`
- Missing GPS: Accept null (device may be indoors)

---

### GET /

**Called by**: Advertiser (web browser)

**Response**: HTML dashboard showing:
- Upload form
- Currently active content
- List of connected devices (last hour)

---

### POST /upload

**Called by**: Advertiser (via web form)

**Request**:
```
POST /upload HTTP/1.1
Host: your-backend.com
Content-Type: multipart/form-data

[JPEG file data]
```

**Response**: Redirect to `/` (dashboard)

**Actions**:
1. Save file to `/uploads/` directory
2. Set all existing content to `active = 0`
3. Insert new content with `active = 1`
4. Devices will pick up on next poll

---

### GET /status

**Called by**: Monitoring system (optional)

**Response**:
```json
{
  "total_devices_seen": 50,
  "online_now": 42,
  "heartbeats_last_hour": 2520
}
```

**Use case**: External monitoring, alerting

---

## Network Topology

```
                    Internet
                       │
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Viettel 4G    Mobifone 4G    Vinaphone 4G
   (Carrier)     (Carrier)      (Carrier)
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │              │              │
        ▼              ▼              ▼
    Taxi 001       Taxi 002       Taxi 050
    (Device)       (Device)       (Device)
```

**Connectivity**:
- Each taxi has independent 4G SIM card
- No device-to-device communication
- All communication goes through backend server
- No VPN, no special networking

**Bandwidth**:
- Heartbeat: ~1KB every 60s = 1.4KB/min
- Content check: ~2KB every 60s = 2.8KB/min
- Image download: ~200KB per update = rare
- **Total**: ~250KB/hour per device = 6MB/day

**Cost**: $3/mo for 5GB = massive buffer

---

## Scaling Characteristics

### MVP (50 devices)
- Database: SQLite (single file)
- Hosting: $5/mo shared instance
- Storage: Local filesystem
- **Total cost**: $5/mo

### Phase 2 (1,000 devices)
- Database: PostgreSQL (managed, $15/mo)
- Hosting: Dedicated instance ($25/mo)
- Storage: S3/R2 (pennies)
- **Total cost**: $50/mo

### Phase 3 (10,000 devices)
- Database: PostgreSQL with read replicas
- Hosting: Load balanced servers ($200/mo)
- Storage: CDN-backed object storage
- **Total cost**: $500/mo

### Full Scale (50,000 devices)
- Database: Clustered PostgreSQL
- Hosting: Kubernetes or managed service
- Storage: Multi-region CDN
- **Total cost**: $2,000-3,000/mo

**Key insight**: Architecture changes at each phase. Don't build for 50,000 when testing 50.

---

## Failure Modes & Handling

### Device Loses 4G Connection
**Symptom**: No heartbeat for >5 minutes
**Impact**: Device shows stale content
**Handling**: Device continues showing last downloaded image
**Recovery**: Automatic when connection restored

### Server Goes Down
**Symptom**: Devices can't reach API
**Impact**: Devices show stale content
**Handling**: Devices retry on next poll (60s later)
**Recovery**: Automatic when server back up

### Image File Corrupted
**Symptom**: Device can't render image
**Impact**: Blank screen on one device
**Handling**: Device logs error, retries download
**Recovery**: Manual - reupload image

### Database Locked (SQLite)
**Symptom**: High concurrent writes fail
**Impact**: Some heartbeats dropped
**Handling**: SQLite busy timeout (5s)
**Recovery**: Automatic retry

### Device Stolen/Broken
**Symptom**: No heartbeat for >24 hours
**Impact**: One device offline
**Handling**: Admin marks device as lost
**Recovery**: Replace hardware

---

## Security Considerations

### For MVP (Low Security)
- ✅ HTTPS for API (free with Railway/Render)
- ✅ No public API keys (server-side only)
- ❌ No authentication (single user, password-protected admin)
- ❌ No device authentication (any device can poll)
- ❌ No content validation (trust uploaded images)

**Risk level**: Low (not handling sensitive data)

### For Production (Higher Security)
- ✅ Device authentication (API keys per device)
- ✅ Content validation (scan for malware/inappropriate)
- ✅ Rate limiting (prevent abuse)
- ✅ Multi-user authentication (advertiser accounts)
- ✅ Audit logging (who uploaded what)

---

## Monitoring & Observability

### MVP Monitoring
**Metrics**:
- Device online count (last 5 min)
- Total heartbeats per hour
- Content update latency

**Tools**:
- Built-in dashboard (GET /)
- Manual SQL queries

**Alerts**: None (manual checks)

### Production Monitoring
**Metrics**:
- Device uptime percentage
- API latency (p50, p95, p99)
- Error rates
- Content delivery success rate
- Geographic coverage map

**Tools**:
- DataDog, New Relic, or similar
- Grafana dashboards
- PagerDuty alerts

---

## Deployment Architecture

### MVP Deployment
```
┌─────────────────────────────┐
│   Railway/Render            │
│   (Managed PaaS)            │
│                             │
│   Single instance:          │
│   - Node.js app             │
│   - SQLite database         │
│   - Local file storage      │
│                             │
│   Auto HTTPS                │
│   Auto deploys from Git     │
└─────────────────────────────┘
```

**Deploy command**: `git push` (automatic)

### Production Deployment
```
┌─────────────────────────────────────────┐
│   Load Balancer                         │
│   (Distributes traffic)                 │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
┌──────────────┐  ┌──────────────┐
│  App Server  │  │  App Server  │
│  (Node.js)   │  │  (Node.js)   │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                │
                ▼
┌───────────────────────────────┐
│   PostgreSQL Database         │
│   (Managed, with replicas)    │
└───────────────────────────────┘
                │
                ▼
┌───────────────────────────────┐
│   CDN (Cloudflare/AWS)        │
│   (Serves static content)     │
└───────────────────────────────┘
```

**But NOT for MVP.** Simple is fast.

---

## Cost Breakdown

### Development (One-time)
- Backend development: $3,000 (1 week)
- Android app development: $3,000 (1 week)
- Testing & iteration: $1,000 (ongoing)
- **Total**: $7,000

### Hardware (Per Device)
- Tablet: $100
- Case: $15
- Power: $5
- SIM: $3/month
- **Total**: $120 + $3/mo

### Operating (Monthly for 50 Devices)
- Server hosting: $5
- Data plans (50 × $3): $150
- **Total**: $155/mo

### 4-Week MVP Total
- Development: $7,000
- Hardware (50 × $120): $6,000
- Operating (1 month): $155
- Contingency: $1,500
- **Total**: $14,655

**Rounded to**: $15,000

---

## Technology Choices: Why This Stack?

### Why Node.js?
- ✅ Fast to build HTTP servers
- ✅ Good ecosystem (Express, multer)
- ✅ Easy to find developers
- ❌ Not the fastest (but fast enough)

**Alternatives considered**:
- Python/Flask: Similar, slightly slower
- Go: Faster but slower to build
- PHP: Viable but less modern

**Decision**: Node.js for speed of development

### Why SQLite?
- ✅ Zero configuration
- ✅ Single file database
- ✅ Sufficient for 50 devices
- ❌ Doesn't scale past ~1,000 devices

**Alternatives considered**:
- PostgreSQL: Better but overkill for MVP
- MySQL: Similar to PostgreSQL
- MongoDB: Wrong data model

**Decision**: SQLite for simplicity, migrate later

### Why Android?
- ✅ Cheap tablets available
- ✅ 4G + GPS built-in
- ✅ Good developer tools
- ❌ Fragmentation issues

**Alternatives considered**:
- iOS: Too expensive, no cheap tablets
- Raspberry Pi: Custom hardware, slower
- E-ink: Limited color, slow refresh

**Decision**: Android for cost and availability

### Why 4G (Not WiFi)?
- ✅ Taxis move around city
- ✅ Can't rely on WiFi availability
- ✅ 4G coverage good in urban Vietnam
- ❌ Ongoing data cost

**Alternatives considered**:
- WiFi-only: Limits to depot updates
- 5G: Overkill and expensive
- LoRaWAN: Too low bandwidth

**Decision**: 4G for mobility

---

## Summary

**Total Code**: 430 lines (backend + device + test)
**Total Docs**: 1,200 lines (specifications, guides, planning)
**Deployment Time**: 4 weeks
**Budget**: $15,000
**Technical Risk**: Validated

This is how you build a feasibility MVP: simple, fast, decisive.
