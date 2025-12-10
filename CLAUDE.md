# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vietnam Taxi DOOH (Digital Out-of-Home) Network - A feasibility MVP to validate remote content distribution to 50,000 taxi screens. The core hypothesis: Can we technically push digital ads to a fleet of taxis via 4G?

## Commands

```bash
# Start the server
cd taxi-mvp && npm start

# Development mode with auto-reload
cd taxi-mvp && npm run dev

# Simulate taxi devices
cd taxi-mvp && node test-client.js
```

Dashboard: http://localhost:3000
Status API: http://localhost:3000/status
Device API: http://localhost:3000/content/:device_id

## Architecture

```
taxi-mvp/
├── server.js              # Express backend (~270 lines)
│   ├── GET /              # Web dashboard (upload form + device status)
│   ├── POST /upload       # Upload JPEG, deploy to fleet
│   ├── GET /content/:id   # Device polls for current content
│   ├── POST /heartbeat    # Device sends GPS + status
│   └── GET /status        # Fleet health JSON
├── test-client.js         # Device simulator
├── android-client.pseudo.kt  # Android app logic reference
├── data/                  # JSON file storage (heartbeats, content)
└── uploads/               # Uploaded ad images
```

**Stack**: Node.js + Express + JSON file storage (deliberately simple - SQLite in docs, JSON in implementation)

**Data flow**: Advertiser uploads JPEG → Server stores file + marks active → Devices poll every 60s → Download and display

## Key Design Decisions

- **Static images only** (no video) - validates distribution, lower bandwidth
- **Polling (60s)** instead of push - simpler, works through NATs/firewalls (validated by GrabAds)
- **JSON file storage** - sufficient for 50 devices, zero config
- **No auth** - single user MVP, add later
- **No programmatic** - manual upload for now
- **Passenger-facing screens only** - headrest-mounted, rear-passenger-only placement eliminates driver distraction (NYC/Singapore/GrabAds precedent)

## MVP Success Criteria

- 80%+ device uptime
- <10 min content update time
- <5% hardware failure rate
- Zero manual interventions

## Research & Strategy Documents

Root directory contains market research and strategy analysis:

### Market Research
- `vietnam-dooh-advertiser-spending-analysis.md` - Top advertiser research
- `existing-solutions-analysis.md` - Competitor analysis
- `[09.12.25]-grabads-taxi-screen-research.md` - GrabAds implementation, safety regulations, Vietnam market (DrivAdz partner, VinaSun 1,500+ screens)
- `how-grab-built-it.md` - Grab's ad server architecture (7-stage pipeline, ElasticSearch, ScyllaDB)

### Business Strategy (09.12.25)
- `[09.12.25]-blue-ocean-*.md/docx` - Blue Ocean Strategy canvases (VPC, BMC)

### Business Model & Financials (11.12.25)
- `[11.12.25]-revenue-estimation-30k-screens.md` - Revenue model: MVP ($10K/mo) to scale ($3.78M/yr)
- `[11.12.25]-pricing-strategy-cpm-cpo-hybrid.md` - Tiered CPM ($4-25) and hybrid CPO mechanics
- `[11.12.25]-xanh-sm-investment-analysis.md` - Xanh SM partnership: $6.12M investment, 70% ROI, 14-mo payback
- `[11.12.25]-mai-linh-idooh-failure-analysis.md` - Why iDOOH failed (execution, not regulations)
- `[11.12.25]-research-summary-hypotheses-findings.md` - Comprehensive hypothesis validation

### Session Tracking
- `session-summaries/` - Session-by-session findings and progress tracking

## Key Validated Insights

### Regulatory (Validated 11.12.25)
- **In-car screens are LEGAL** - Article 32, Advertising Law 2012
- **No license required** - Only notification (15 days, auto-approved)
- **Passenger-facing placement** - Headrest-mounted screens don't distract drivers

### Why Previous Attempts Failed (iDOOH + Mai Linh)
- Mai Linh had $8M debt when partnership formed (2018)
- iDOOH funded hardware themselves - burned $3.88M
- No ride data integration - couldn't target or prove ROI
- **Lesson**: Partner with growing fleet (Xanh SM), they fund hardware

### Unit Economics (Validated 11.12.25)
- MVP break-even: 7% fill rate
- Scale target: 40% fill rate = $3.78M/year profit
- Xanh SM ROI: 70% over 3 years (14-month payback)

## Custom Agents

Three specialized agents in `.claude/agents/`:

- **adtech-cto-founder** - Programmatic advertising architecture decisions, simplifying complex adtech into minimal solutions
- **vietnam-dooh-research-expert** - Vietnam DOOH market intelligence, pricing, suppliers, competitive analysis
- **research-visualizer** - Transform Markdown research into Word docs with data visualizations
