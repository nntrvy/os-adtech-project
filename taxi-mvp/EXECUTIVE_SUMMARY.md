# Executive Summary: Taxi DOOH Feasibility MVP

## The Question

**Can we reliably push digital content to 50,000 taxi screens across Vietnam?**

Not "will advertisers buy?" or "will it make money?" - but "can we technically execute this?"

---

## The Answer: Build This MVP

### What It Does
- Upload JPEG ad to web interface
- Push to 50 taxi screens via 4G
- Verify content is displaying

### What It Proves
- Hardware survives Vietnam taxi operations
- 4G connectivity is reliable enough
- Remote updates work without manual intervention
- System can operate at scale

### Timeline
**4 weeks** from funding to results

### Budget
**$15,000** (~$300/taxi for 30-day validation)

### Success Criteria
- 80%+ device uptime
- <10 min content update time
- <5% hardware failure rate
- Zero manual interventions

---

## Why This Is The Right MVP

### 1. Tests The Hardest Risk
The technical unknowns:
- Will tablets survive heat/rain/vibration?
- Is 4G coverage good enough?
- Can we push updates reliably?
- What's the real failure rate?

**Market risk is LOW** (demand exists, proven by $130M Vietnam DOOH market).
**Technical risk is HIGH** (unproven at this scale in Vietnam).

Test the high-risk assumption first.

### 2. Minimum Viable Validation
We're NOT building:
- Video playback (images prove the concept)
- Programmatic bidding (manual uploads work for test)
- Analytics dashboard (raw logs sufficient)
- Multi-advertiser platform (single user MVP)

**Ruthlessly simple**. Every feature cut reduces time to validation.

### 3. Fast Learning
- Week 1: Know if hardware survives
- Week 2: Know if software works
- Week 3: Know if it scales to 50 devices
- Week 4: Know actual costs and failure rates

**30 days to definitive answer**: proceed or pivot.

### 4. Low Capital Risk
$15k is tiny compared to:
- Custom hardware development: $200k+
- Full platform build: $500k+
- 1,000-taxi rollout: $300k+

**Learn for 2% of the cost** of a full deployment.

---

## The Tech Stack (Deliberately Simple)

### Hardware
- **Screen**: $100 Android tablet (not custom hardware)
- **Case**: $15 waterproof case (not engineered enclosure)
- **Power**: $5 car battery adapter (not solar panel system)
- **Connectivity**: $3/mo prepaid SIM (not IoT platform)

**Why cheap components**: We're testing IF it works, not building production units.

### Software
- **Backend**: Node.js + SQLite on $5/mo hosting
- **Device**: Simple Android app polling server every 60s
- **Storage**: Free CDN tier

**Why simple stack**:
- 200 lines of code vs 20,000
- Zero framework dependencies
- One developer can build it in a week
- Easy to debug and modify

---

## What Happens After Validation

### If We Hit Success Criteria (80%+ uptime)

**Month 2-3**: Scale to 1,000 taxis
- Bulk order custom hardware ($50/unit)
- Build advertiser self-serve platform
- Hire 2 sales people
- Run first paid campaigns

**Funding needed**: $300k

**Month 4-12**: Scale to 10,000 taxis
- Integrate programmatic bidding
- Connect to ad exchanges
- Expand to Hanoi
- Revenue target: $100k/month

**Funding needed**: $2M Series A

**Month 12-24**: Full deployment (50,000 taxis)
- National coverage
- Multiple ad formats (video, interactive)
- Enterprise sales team
- Revenue target: $2-3M/month

### If We Don't Hit Success Criteria

**Pivot options**:
1. **WiFi-only updates**: Taxis update at depot, not real-time
2. **Static wraps**: Non-digital taxi advertising (simpler tech)
3. **In-car displays**: Target passengers instead of external viewers
4. **Different vehicle type**: Buses, trucks, delivery vehicles

**Key insight**: $15k to learn BEFORE committing $300k+

---

## Competitive Advantages

### 1. Exclusive Distribution
50,000 vehicles = largest mobile DOOH network in Vietnam.

Competitor would need:
- Years to sign up equivalent fleet
- OR build relationship with XanhSM (we have it)

**Moat**: Distribution access

### 2. First-Mover in Vietnam
No programmatic taxi DOOH in Vietnam yet.

Benefits:
- Land top advertisers first
- Set pricing expectations
- Build brand recognition

**Moat**: Market timing

### 3. Lean Technical Approach
We can validate for $15k what others would spend $500k on.

Benefits:
- Faster iteration
- Less capital at risk
- More shots on goal

**Moat**: Execution speed

---

## Risk Analysis

### Technical Risks (MVP Tests These)
- ❓ Hardware failure rate → **Testing in Week 1-3**
- ❓ 4G coverage gaps → **Testing in Week 1-3**
- ❓ Update latency → **Testing in Week 2-4**
- ❓ Operating costs → **Measuring in Week 1-4**

### Market Risks (NOT Testing Yet)
- ❓ Advertiser demand → Test in Phase 2 with first paid campaign
- ❓ Viewability/attention → Test in Phase 2 with brand study
- ❓ Pricing/monetization → Test in Phase 2 with real campaigns

### Regulatory Risks (Low)
- ✅ Digital screens on vehicles legal in Vietnam
- ✅ No special advertising licenses needed for MVP
- ✅ Privacy regulations not applicable (no personal data)
- ⚠️ Monitor: Traffic distraction regulations (not enforced currently)

---

## Decision Framework

### Proceed to Phase 2 if:
- 80%+ device uptime
- <10 min update latency
- <$10/month operating cost per device
- At least 1 advertiser willing to pay for test campaign

### Pivot if:
- <60% device uptime (hardware not viable)
- >30 min update latency (UX too poor)
- >$20/month operating cost (economics don't work)
- Zero advertiser interest (wrong product)

### Kill if:
- <40% device uptime (fundamentally broken)
- Regulatory issues emerge
- Competitor launches equivalent with better economics

---

## The Ask

**$15,000 for 4-week technical validation**

In exchange:
- 50 taxis with working screens
- 30 days of operational data
- Definitive answer on technical feasibility
- Clear decision point: proceed or pivot

**Risk**: $15k (tiny)
**Reward**: Validated path to $10M+ business (huge)
**Timeline**: 30 days to answer

---

## Next Steps

### Week 1
- Wire funds → $15k
- Source hardware → 3 test units
- Install on taxis → Day 3-4
- Stress test → Day 5-7

### Week 2
- Build software → Backend + Android app
- Deploy to 3 taxis → Test updates
- Validate end-to-end → Push content remotely

### Week 3
- Scale to 50 taxis → Order hardware
- Install fleet → Assembly-line install day
- Monitor operations → Track uptime/failures

### Week 4
- Run demo campaign → Real advertiser
- Package results → Investor presentation
- Decision meeting → Proceed to Phase 2?

---

## Why This Will Work

**1. Problem is real**: Vietnam DOOH market growing 12.54% annually

**2. Solution is feasible**: Similar models work globally (Grab, Firefly, etc)

**3. Distribution is exclusive**: 50,000-vehicle head start on competitors

**4. Team can execute**: [Your credentials]

**5. Risk is minimal**: $15k to validate, not $500k to build

**6. Upside is massive**: $10M+ revenue potential if validated

---

## Comparable Exits

- **Firefly** (US taxi-top ads): Raised $21.5M, acquired by EcoMedia
- **Vugo** (rideshare screens): Raised $10M Series A
- **Adomni** (programmatic DOOH): Raised $13M, acquired by Viant
- **Vistar Media** (DOOH exchange): Raised $17M

**Vietnam DOOH is underserved**. No equivalent platform exists yet.

---

## Bottom Line

**This is the simplest possible test of the hardest technical risk.**

Not over-engineered. Not premature scaling. Just:
- 50 taxis
- 4 weeks
- $15k
- Clear success criteria

Then decide: scale or pivot.

**Low risk. High learning. Fast execution.**

That's how you validate feasibility before building a business.
