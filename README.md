# Vietnam Taxi DOOH Network

**Feasibility MVP: Can we push digital ads to 50,000 taxis?**

---

## Project Structure

```
/Users/nntrvy/os-adtech-project/
├── taxi-mvp/                      # MVP implementation
│   ├── server.js                  # Backend (200 lines)
│   ├── package.json               # Dependencies
│   ├── test-client.js             # Device simulator
│   ├── android-client.pseudo.kt   # Android app logic
│   │
│   ├── EXECUTIVE_SUMMARY.md       # Start here (decision makers)
│   ├── INVESTOR_BRIEF.md          # Full investor pitch
│   ├── DEPLOYMENT.md              # 4-week execution plan
│   ├── HARDWARE_SPEC.md           # Component details
│   └── README.md                  # Technical quickstart
│
└── README.md                      # This file
```

---

## Quick Start (5 Minutes)

### 1. Read The Strategy
```bash
cat taxi-mvp/EXECUTIVE_SUMMARY.md
```
**Why**: Understand the core hypothesis and validation approach

### 2. See The Tech
```bash
cd taxi-mvp
npm install
npm start
```
Open http://localhost:3000

### 3. Simulate A Device
```bash
node test-client.js
```
Watch heartbeats appear in dashboard

### 4. Test Content Push
- Open http://localhost:3000
- Upload a JPEG image
- See it deploy to simulated device

---

## The Core Idea

**Problem**: Vietnam has a $130M DOOH market but limited digital inventory

**Opportunity**: 50,000 XanhSM taxis = mobile billboards

**Risk**: Can we technically execute this?

**Solution**: 4-week MVP to validate hardware + connectivity at scale

---

## What's Inside

### `/taxi-mvp/server.js` (200 lines)
- Upload ad images
- Push to device fleet
- Track device heartbeats
- Monitor uptime

**Tech**: Node.js + Express + SQLite (deliberately simple)

### `/taxi-mvp/android-client.pseudo.kt` (100 lines)
- Display fullscreen images
- Poll server every 60s
- Send GPS heartbeat
- Auto-restart on crash

**Tech**: Android + Kotlin (or React Native)

### Documents
- **EXECUTIVE_SUMMARY.md**: Decision-maker overview (10 min read)
- **INVESTOR_BRIEF.md**: Full pitch deck (20 min read)
- **DEPLOYMENT.md**: Week-by-week build plan (30 min read)
- **HARDWARE_SPEC.md**: Component sourcing guide (30 min read)

---

## Timeline

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Hardware validation | 3 taxis survive stress test |
| 2 | Software build | Remote content push works |
| 3 | Scale to 50 | 80%+ fleet uptime |
| 4 | Investor demo | Technical feasibility proven |

---

## Budget

| Item | Amount |
|------|--------|
| Hardware (50 units) | $6,500 |
| Labor (dev + ops) | $7,000 |
| Contingency | $1,500 |
| **Total** | **$15,000** |

**Cost per taxi**: $300 for 30-day validation

---

## Success Criteria

We've validated feasibility if:
- ✅ 80%+ device uptime
- ✅ <10 min content update time
- ✅ <5% hardware failure rate
- ✅ Zero manual interventions

---

## Key Design Decisions

### Why Android Tablets (Not Custom Hardware)?
- Available off-the-shelf in Vietnam
- 4G + GPS built-in
- $100 vs $500 for custom
- Fast to test, easy to replace

**Trade-off**: Accept higher failure rate to validate faster

### Why Static Images (Not Video)?
- Proves content distribution works
- Lower bandwidth requirements
- Simpler to debug

**Trade-off**: Less engaging ads, but sufficient for feasibility test

### Why Manual Upload (Not Programmatic)?
- MVP has 1 advertiser
- Manual process takes 2 minutes
- Programmatic takes 4 weeks to build

**Trade-off**: Doesn't scale, but not testing scale yet

### Why SQLite (Not PostgreSQL)?
- 50 devices = tiny data volume
- Zero ops complexity
- Faster iteration

**Trade-off**: Migration needed later, but premature for MVP

---

## What We're NOT Building

❌ Video playback
❌ Programmatic bidding
❌ Analytics dashboard
❌ Campaign scheduling
❌ Multi-tenant platform
❌ Payment processing
❌ Mobile app for advertisers
❌ Viewability tracking
❌ A/B testing
❌ Geo-targeting

**All of these come AFTER we prove basic content distribution works.**

---

## Risk Mitigation

### Technical Risks
- **Overheating**: White cases, ventilation holes
- **Water damage**: IP65 cases, silicone seals
- **Theft**: Secure mounting, 10% replacement budget
- **4G coverage**: Test in target zones first

### Market Risks (Not Testing Yet)
- **Demand**: Validate in Phase 2 with paid campaign
- **Pricing**: Test in Phase 2 with multiple brands
- **Viewability**: Study in Phase 2 with brand lift analysis

---

## Next Phase (If Validated)

**Phase 2: 1,000 Taxi Launch** ($300k, 3 months)
- Custom hardware manufacturing
- Advertiser self-serve platform
- Sales team (2 people)
- Real revenue campaigns

**Phase 3: Programmatic Scale** ($2M, 12 months)
- 10,000 taxis
- OpenRTB integration
- Ad exchange partnerships
- $100k/mo revenue target

---

## Competitive Landscape

**Global comparables**:
- Firefly (US): Taxi-top LED screens
- Vugo (Global): Rideshare in-car tablets
- Grab (SEA): In-car displays for passengers

**Vietnam**: No direct competitor yet (first-mover advantage)

**Defensibility**: Exclusive access to 50,000-vehicle fleet

---

## Team Requirements

### For MVP (Week 1-4)
- 1x Full-stack developer (build backend + Android app)
- 1x Operations person (install hardware, coordinate taxis)
- 1x Technical lead (you) to manage and decide

### For Phase 2 (If Validated)
- 2x Sales people
- 1x Backend engineer
- 1x Mobile engineer
- 1x Operations manager

---

## Key Questions This MVP Answers

1. ✅ Does hardware survive taxi operations?
2. ✅ Is 4G connectivity reliable in target zones?
3. ✅ Can we update content remotely without manual intervention?
4. ✅ What's the real operating cost per taxi?
5. ✅ What's the actual failure/replacement rate?
6. ✅ Will advertisers pay for this inventory?

---

## Key Questions This MVP Does NOT Answer

1. ❌ What's the optimal ad pricing? (Phase 2)
2. ❌ How do we measure viewability? (Phase 2)
3. ❌ Can we integrate programmatically? (Phase 2)
4. ❌ What's the right sales model? (Phase 2)

**Deliberately narrow scope = faster learning**

---

## Files You Should Read (In Order)

### 1. EXECUTIVE_SUMMARY.md (Start Here)
High-level strategy and decision framework

### 2. INVESTOR_BRIEF.md
Full pitch with market analysis and financial model

### 3. DEPLOYMENT.md
Week-by-week execution plan

### 4. HARDWARE_SPEC.md
Component sourcing and assembly instructions

### 5. server.js
The actual code (only 200 lines)

---

## Running The Demo

### Terminal 1: Start Server
```bash
cd taxi-mvp
npm install
npm start
```

### Terminal 2: Simulate Device
```bash
cd taxi-mvp
node test-client.js
```

### Browser: Control Panel
Open http://localhost:3000

### Test Flow
1. Upload a JPEG image
2. Watch test-client.js log "Content available: [URL]"
3. See device appear in "Connected Devices" section
4. Upload new image, watch it update

**This is exactly what happens on real taxis, just without hardware.**

---

## Deployment to Production

### Backend (Railway/Render)
```bash
git init
git add .
git commit -m "Initial commit"

# Deploy to Railway
railway login
railway init
railway up

# Or deploy to Render
# Push to GitHub, connect in Render dashboard
```

### Android App
1. Build in Android Studio
2. Export APK
3. Load onto tablets via USB or Google Drive link
4. Configure server URL before deployment

### Hardware Installation
See DEPLOYMENT.md for detailed checklist

---

## Contact & Support

**Technical questions**: [Your email]
**Investment inquiries**: [Your email]
**Hardware sourcing**: See HARDWARE_SPEC.md vendor list

---

## License

Proprietary - All rights reserved

---

## Philosophy

This MVP embodies a core principle:

**"Build the minimum that validates the maximum risk."**

We're not building a complete ad platform. We're testing: **Can we do it technically?**

Every feature not in this MVP is intentionally cut to:
- Reduce time to validation (4 weeks, not 6 months)
- Reduce capital at risk ($15k, not $500k)
- Maximize learning velocity (test one thing well)

Once we prove feasibility, we build the business.

But NOT before.

---

## What Success Looks Like

**End of Week 4**:
- 50 taxis with working screens
- 80%+ uptime over 30 days
- Content updates within 10 minutes
- Real advertiser ran test campaign
- Definitive data on costs and failure rates

**Then**: Raise $300k for 1,000-taxi deployment

**Not now**: Build before validating

---

**This is how you de-risk a hardware-dependent adtech business.**

Simple. Fast. Decisive.
