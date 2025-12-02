# 4-Week Deployment Plan

## Week 1: Hardware Validation (3 Taxis)

### Day 1-2: Hardware Sourcing
- [ ] Purchase 3x Android tablets in HCMC
  - Recommended: Samsung Galaxy Tab A8 or equivalent
  - Screen size: 10-10.5 inches
  - Must have 4G LTE support
  - Cost: ~$100-120 USD each

- [ ] Get waterproof cases
  - Look for motorcycle/scooter phone mounts (Vietnam has many)
  - Must withstand rain and heat
  - Cost: ~$10-20 each

- [ ] Get 3x prepaid 4G SIM cards
  - Viettel (best coverage) or Mobifone
  - 5GB/month data plan
  - Cost: ~$3/month

- [ ] Get power adapters
  - 12V car battery to 5V USB converter
  - 2A minimum output
  - Cost: ~$5 each

### Day 3-4: Installation
- [ ] Install hardware on 3 test taxis
  - Mount case to roof (zip ties work for MVP)
  - Wire power to car battery (ask taxi mechanic)
  - Insert SIM cards
  - Install Android APK

- [ ] Configure each device
  - Set unique device_id (taxi_001, taxi_002, taxi_003)
  - Set server URL
  - Disable auto-sleep
  - Set brightness to 100%

### Day 5-7: Stress Testing
- [ ] Deploy backend to Railway/Render
- [ ] Upload test image
- [ ] Have taxis drive 8 hours/day
- [ ] Monitor issues:
  - Screen overheating?
  - Power drainage?
  - 4G dropouts?
  - Waterproofing leaks?

**Success Criteria**: All 3 tablets survive 3 days, receive content updates

---

## Week 2: Software Build & Testing

### Day 1-3: Build Android App
- [ ] Set up Android Studio project
- [ ] Implement core features:
  - Fullscreen image display
  - HTTP polling every 60s
  - Heartbeat sender
  - GPS location tracking
  - Auto-restart on crash

- [ ] Build APK
- [ ] Test on 3 existing devices

### Day 4-5: Refine Backend
- [ ] Deploy production server
- [ ] Test content distribution:
  - Upload image
  - Verify all 3 devices update within 5 min
  - Check heartbeat logs

- [ ] Add basic monitoring
  - Device online/offline detection
  - Alert if device goes dark for >30 min

### Day 6-7: Integration Testing
- [ ] Push 5 different ad creatives throughout day
- [ ] Verify update speed
- [ ] Monitor 4G data usage per device
- [ ] Check GPS tracking accuracy

**Success Criteria**: Can reliably push content to 3 moving taxis

---

## Week 3: Scale to 50 Taxis

### Day 1-2: Hardware Setup
- [ ] Order 47 more tablets (bulk purchase)
- [ ] Order 47 more SIM cards
- [ ] Prepare 47 power kits
- [ ] Mass-install APKs with unique device IDs

### Day 3: Installation Day
- [ ] Schedule 50 taxis to come to central location
- [ ] Install hardware assembly-line style
- [ ] Test each device before taxi leaves
- [ ] Document device_id → taxi license plate mapping

### Day 4-7: Monitoring Period
- [ ] Daily checks:
  - How many devices reported in last hour?
  - How many failed to update content?
  - Any hardware failures?

- [ ] Fix issues:
  - Replace broken tablets
  - Troubleshoot connectivity problems
  - Adjust power connections if needed

**Success Criteria**: 40+ devices (80%) reliably online

---

## Week 4: Investor Demo

### Day 1: Get Real Advertiser
- [ ] Approach 1 local brand (coffee, telecom, bank)
- [ ] Get their creative (JPEG ad)
- [ ] Negotiate test campaign: $500 for 3 days

### Day 2-4: Run Live Campaign
- [ ] Upload brand's creative
- [ ] Monitor deployment across fleet
- [ ] Track metrics:
  - Number of devices showing ad
  - Geographic coverage (HCMC districts)
  - Uptime percentage

### Day 5: Prepare Investor Materials
- [ ] Create simple presentation:
  - "We deployed ads to 50 moving taxis"
  - Map showing device locations
  - Uptime/reliability metrics
  - Screenshots of admin panel

- [ ] Record demo video:
  - Show tablet on taxi roof
  - Show web UI pushing content
  - Show ad appearing on screen within minutes

**Deliverable**: Proof that technical feasibility is validated

---

## Installation Checklist (Per Taxi)

### Hardware Setup
1. Attach waterproof case to roof
   - Use heavy-duty zip ties or small bolts
   - Ensure case opens for USB access

2. Connect power
   - Run wire from car battery to roof
   - Use 12V-to-5V converter
   - Secure wiring with zip ties
   - Test: tablet charges when engine on

3. Configure tablet
   - Insert 4G SIM card
   - Install APK from USB drive
   - Set device_id: taxi_XXX
   - Set server URL
   - Test: open app, see placeholder image

4. Test connectivity
   - Drive 5 minutes
   - Check admin panel: heartbeat received?
   - Push test image: updates within 5 min?

5. Finalize
   - Close waterproof case
   - Document device_id + license plate
   - Give driver contact number for issues

**Time per installation**: ~30 minutes

---

## Troubleshooting Guide

### Device not reporting heartbeat
1. Check 4G SIM has data
2. Check app is running (not crashed)
3. Check server URL is correct
4. Check power connection

### Content not updating
1. Check device received heartbeat recently
2. Check image URL is accessible
3. Restart app on device
4. Check 4G connectivity

### Screen blank/black
1. Check power connection
2. Check tablet battery not dead
3. Check app didn't crash
4. Reboot tablet

### High failure rate
- If >20% devices offline: likely 4G coverage issue
- If specific devices failing: likely hardware issue
- If all devices fail to update: likely server issue

---

## Cost Tracking (50 Devices)

| Item | Qty | Unit Cost | Total |
|------|-----|-----------|-------|
| Android tablets | 50 | $110 | $5,500 |
| Waterproof cases | 50 | $15 | $750 |
| Power adapters | 50 | $5 | $250 |
| 4G SIM cards (1 mo) | 50 | $3 | $150 |
| Backend hosting | 1 | $5 | $5 |
| Labor (install) | - | - | $1,000 |
| Replacements (10%) | - | - | $500 |
| **TOTAL** | | | **$8,155** |

**Cost per taxi**: ~$163 for 30-day validation

If validated, expect costs to drop to ~$80/taxi with bulk manufacturing.

---

## Risk Mitigation

### Risk: Tablets overheat in Vietnam sun
- Mitigation: Test with white reflective case, add ventilation holes
- Fallback: Use industrial-grade tablets ($250 each)

### Risk: 4G coverage insufficient
- Mitigation: Test in target districts first, map dead zones
- Fallback: Use WiFi-only updates when taxis return to depot

### Risk: Tablets get stolen
- Mitigation: Mount securely, make case hard to remove
- Fallback: Budget for 10-20% replacement rate

### Risk: Battery drainage
- Mitigation: Test power draw, ensure converter adequate
- Fallback: Add larger backup battery

### Risk: Drivers disconnect devices
- Mitigation: Educate drivers, offer incentive ($10/mo) for uptime
- Fallback: Detect tampering via heartbeat gaps

---

## Next Phase (If Validated)

Once we hit 80%+ uptime with 50 taxis:

1. **Custom Hardware** ($5k investment)
   - Design custom Android device ($50 cost)
   - Better weatherproofing
   - Built-in GPS + 4G
   - 5-year lifespan

2. **Advertiser Dashboard** (2 weeks)
   - Self-serve campaign creation
   - Real-time reporting
   - Payment integration

3. **Programmatic Bidding** (4 weeks)
   - OpenRTB integration
   - Connect to Vietnamese ad exchanges
   - Automated pricing

4. **Scale to 5,000 taxis** (3 months)
   - Bulk hardware manufacturing
   - Field installation team
   - 24/7 monitoring

But NOT before we prove feasibility with 50.
