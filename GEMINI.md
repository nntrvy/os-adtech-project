# Gemini Project Context: Vietnam Taxi DOOH Ad Platform

This document provides a summary of the current project to be used as instructional context for future interactions.

**Last Updated**: 2025-12-03

## Project Status: MVP COMPLETED

This directory contains a **fully functional MVP** for distributing digital advertisements to taxi-mounted screens in Vietnam, targeting the 50,000-vehicle XanhSM taxi fleet.

## Project Evolution

**Phase 1 (Completed)**: Planning and Architecture
- Initial technical blueprint in `ad_tech_backend.md`
- Microservices architecture design
- Technology stack selection

**Phase 2 (Completed)**: MVP Development
- Built working Node.js backend server (`/taxi-mvp/server.js`)
- Created device simulation and testing tools
- Implemented content distribution system
- Built real-time monitoring dashboard

**Phase 3 (Completed)**: Documentation and Research
- Comprehensive business and technical documentation
- Vietnam DOOH market research with visualizations
- Investor-ready pitch materials
- Hardware specifications and deployment guide

## Directory Overview

### Core MVP Implementation (`/taxi-mvp/`)
The working code for the feasibility MVP:

- **server.js** (274 lines): Express.js backend with image upload, device heartbeat tracking, content distribution API, and real-time dashboard
- **test-client.js**: Device simulator for testing
- **android-client.pseudo.kt**: Pseudocode for Android app implementation
- **package.json**: Dependencies (express, multer)

### Business Documentation (`/taxi-mvp/`)
Investor and stakeholder materials:

- **EXECUTIVE_SUMMARY.md**: Decision-maker overview (10-min read)
- **INVESTOR_BRIEF.md**: Full pitch deck with market analysis
- **DEPLOYMENT.md**: 4-week execution plan
- **HARDWARE_SPEC.md**: Android tablet component sourcing
- **ARCHITECTURE.md**: Technical design and decisions
- **GETTING_STARTED.md**: Developer quickstart

### Market Research
Comprehensive Vietnam DOOH analysis:

- **vietnam-dooh-advertiser-spending-analysis.md**: $130M market analysis
- **charts-and-graphs/**: 7 professional visualizations (PNG format)
- Multiple `.docx` reports with embedded charts
- Python scripts for visualization generation

### AI Agent Configuration (`.claude/agents/`)
Specialized assistants for this project:

- **adtech-cto-founder.md**: Technical architecture and code review expert
- **vietnam-dooh-research-expert.md**: Market research specialist
- **research-visualizer.md**: Data visualization expert

### Technical Planning
Reference architectures for future phases:

- **ad_tech_backend.md**: Comprehensive backend blueprint for production scale
  - Microservices architecture (Ad Management, Ad Selection, Event Tracking)
  - Technology stack: Python/FastAPI, PostgreSQL+PostGIS, Redis, Kafka
  - OpenRTB integration planning
  - Geo-targeting and programmatic bidding design

## Current System Capabilities

### What Works NOW (MVP)
1. Upload JPEG/PNG images via web interface
2. Automatically deploy content to entire taxi fleet
3. Receive GPS-enabled heartbeats from devices every 60 seconds
4. Real-time dashboard showing:
   - Active device count
   - Online/offline status
   - Content deployment status
   - Last-seen timestamps
5. Device fleet monitoring and health metrics
6. JSON-based persistence for rapid iteration

### Success Criteria (4-Week Validation)
- 80%+ device uptime (hourly heartbeats)
- <10 minute content update time
- <5% hardware failure rate
- Zero manual interventions

### Technology Stack (MVP)
- **Backend**: Node.js + Express
- **Storage**: JSON files (heartbeats.json, content.json)
- **File Upload**: Multer
- **Device**: Android tablets with 4G + GPS
- **Deployment**: Railway/Render ready

## MVP Philosophy

**Core Principle**: "Build the minimum that validates the maximum risk"

### What We Built
✓ Static image distribution
✓ Device heartbeat tracking
✓ Manual upload interface
✓ Basic fleet monitoring
✓ File-based storage

### What We Intentionally Skipped
✗ Video playback (Phase 2)
✗ Programmatic bidding (Phase 2)
✗ Analytics dashboard (Phase 2)
✗ Campaign scheduling (Phase 2)
✗ Multi-tenant platform (Phase 2)
✗ Payment processing (Phase 2)
✗ Viewability tracking (Phase 2)
✗ A/B testing (Phase 2)
✗ Geo-targeting (Phase 2)

## Project Economics

**MVP Budget**: $15,000
- Hardware (50 units): $6,500
- Labor: $7,000
- Contingency: $1,500

**Timeline**: 4 weeks to validate feasibility

**Phase 2** (If validated): $300K for 1,000 taxis
**Phase 3** (If successful): $2M for 10,000 taxis + programmatic scale

## Market Opportunity

- **Market Size**: $130M Vietnam DOOH market
- **Target Fleet**: 50,000 XanhSM taxis
- **Competition**: No direct competitor in Vietnam (first-mover advantage)
- **Defensibility**: Exclusive fleet access

## Usage Guide

### Quick Start
```bash
cd /Users/nntrvy/os-adtech-project/taxi-mvp
npm install
npm start
```

Then:
1. Open http://localhost:3000 for dashboard
2. Run `node test-client.js` to simulate devices
3. Upload images to test content distribution

### API Endpoints
- `GET /content/:device_id` - Device polls for current content
- `POST /heartbeat` - Device sends status update
- `GET /` - Web dashboard
- `POST /upload` - Upload new content
- `GET /status` - Fleet health JSON

## Key Files Reference

### For Business Stakeholders
1. `/taxi-mvp/EXECUTIVE_SUMMARY.md` - Start here
2. `/taxi-mvp/INVESTOR_BRIEF.md` - Full pitch
3. `/README.md` - Project overview

### For Developers
1. `/taxi-mvp/GETTING_STARTED.md` - Quick start
2. `/taxi-mvp/server.js` - The actual code (274 lines)
3. `/taxi-mvp/ARCHITECTURE.md` - Design decisions

### For Future Planning
1. `/ad_tech_backend.md` - Production architecture blueprint
2. `/SESSION-SUMMARY.md` - Complete development history

## Next Steps

**Immediate** (Hardware Validation):
1. Procure 3 Android tablets per HARDWARE_SPEC.md
2. Install 4G SIM cards
3. Run 1-week stress test in taxis
4. Measure actual failure rates

**Phase 2** (If MVP Validates):
1. Scale to 50 taxis
2. Add video playback
3. Build advertiser dashboard
4. Implement basic geo-targeting
5. Launch first paid campaign

**Phase 3** (If Market Validates):
1. Custom hardware manufacturing
2. OpenRTB integration
3. Programmatic bidding
4. Ad exchange partnerships
5. Scale to 10,000 taxis

## Session History

See `/SESSION-SUMMARY.md` for detailed development history.

**Latest Session**: 2025-12-03
- Built complete MVP system
- Generated all documentation
- Created market research and visualizations
- Configured AI agents
- Ready for hardware testing

## Important Notes

- **Git Status**: Not yet initialized (recommend initializing before hardware phase)
- **Testing**: Device simulator functional, ready for field testing
- **Documentation**: All investor and technical docs complete
- **Deployment**: Railway/Render ready, just need BASE_URL env var

---

Future tasks should use:
1. `ad_tech_backend.md` for production architecture guidance
2. `/taxi-mvp/ARCHITECTURE.md` for MVP technical decisions
3. `.claude/agents/adtech-cto-founder.md` for technical reviews
4. This file (GEMINI.md) for project context
