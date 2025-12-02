# Hardware Specification: MVP Taxi Display Unit

## Overview

Simple, off-the-shelf components for 4-week feasibility test. NOT final production hardware.

---

## Component List (Per Taxi)

### 1. Display Device: Android Tablet

**Recommended Models** (available in Vietnam):

**Option A: Samsung Galaxy Tab A8 10.5"** (~$120 USD)
- Screen: 10.5" LCD, 1920x1200
- Processor: Unisoc Tiger T618
- Storage: 32GB (sufficient for MVP)
- RAM: 3GB
- 4G LTE: Yes (required)
- Battery: 7,040mAh
- Weight: 508g

**Option B: Huawei MatePad T10s** (~$100 USD)
- Screen: 10.1" IPS, 1920x1200
- Processor: Kirin 710A
- Storage: 32GB
- RAM: 2GB
- 4G LTE: Yes
- Battery: 5,100mAh
- Weight: 450g

**Option C: Chinese Generic Tablet** (~$80 USD)
- Look for: 10" screen, 4G LTE, 3GB RAM minimum
- Brands: Alldocube, Teclast, Chuwi
- Risk: Lower build quality, but acceptable for MVP

**Decision criteria**: Pick whatever is cheapest with 4G LTE. We're testing feasibility, not building production units.

---

### 2. Weatherproof Case

**Option A: Generic Waterproof Case** (~$15 USD)
- Search: "motorcycle phone holder waterproof"
- Must fit 10" tablet
- IP65 rating minimum (dust + water resistant)
- Clear front window
- Accessible charging port

**Option B: DIY Solution** (~$10 USD)
- Clear plastic food storage container
- Cut hole for charging cable
- Seal with silicone
- Mount with zip ties

**For MVP**: Either works. DIY is fine if commercial cases too expensive.

**Key requirements**:
- Transparent front (for screen visibility)
- Water-resistant (Vietnam rain)
- Heat ventilation (prevent overheating)
- Easy to open (for troubleshooting)

---

### 3. Power Supply

**12V to 5V USB Converter** (~$5 USD)
- Input: 12V DC (car battery)
- Output: 5V DC, 2A minimum (10W)
- Recommended: 5V 3A (15W) for margin
- Look for: "car USB charger adapter hardwire kit"

**Wiring**:
- Connect to car battery positive/negative terminals
- Run wire along car body to roof
- Use inline fuse (3A) for safety
- Secure with zip ties

**Backup Power**:
- Tablet's built-in battery (5,000-7,000mAh)
- Provides ~4-6 hours runtime if car battery disconnected
- Sufficient for MVP (taxis run 8-12 hrs/day)

---

### 4. Connectivity: 4G SIM Card

**Recommended Carrier: Viettel** (best coverage)
- Plan: Prepaid data-only
- Data: 5GB/month
- Cost: ~$3/month
- Speed: 4G LTE (10-50 Mbps typical)

**Alternative Carriers**:
- Mobifone: Similar coverage, slightly cheaper
- Vinaphone: Good in cities, weaker rural

**Data usage estimate**:
- Heartbeat every 60s: ~1KB each = 43MB/month
- Content check every 60s: ~2KB each = 86MB/month
- Image download: ~200KB per ad = 200KB × 30 updates/month = 6MB
- **Total**: ~135MB/month (5GB is huge buffer)

**SIM card setup**:
- Buy prepaid SIM at local store
- Register with ID (Vietnam requirement)
- Activate data plan
- Insert into tablet
- Disable voice/SMS (data only)

---

### 5. Mounting Hardware

**Option A: Zip Ties** (~$5 for pack of 100)
- Use heavy-duty UV-resistant zip ties
- Attach case to taxi roof rack
- Pros: Cheap, easy to install/remove
- Cons: Not theft-proof

**Option B: Small Bolts** (~$10)
- Drill small holes in taxi roof
- Bolt case securely
- Pros: More secure
- Cons: Permanent modification

**For MVP**: Zip ties are fine. We're testing 4 weeks, not 4 years.

---

## Assembly Instructions

### Step 1: Prepare Tablet (5 minutes)
1. Charge tablet fully
2. Insert 4G SIM card
3. Power on, complete Android setup
4. Install APK from USB drive or Google Drive link
5. Configure app:
   - Device ID: taxi_001 (unique per taxi)
   - Server URL: https://your-backend.com
6. Disable sleep mode (Settings → Display → Screen timeout → Never)
7. Set brightness to 100%
8. Enable auto-restart on power (Developer options)

### Step 2: Wire Power (15 minutes)
1. Locate car battery (usually under hood or under seat)
2. Connect red wire to positive terminal
3. Connect black wire to negative terminal
4. Add inline fuse (3A)
5. Run wire through car body to roof
6. Connect USB converter
7. Test: Plug in tablet, should charge

### Step 3: Mount Case (10 minutes)
1. Place tablet in waterproof case
2. Route power cable through case port
3. Seal case
4. Attach case to taxi roof rack with zip ties
5. Position screen facing backward (for following traffic)
6. Test: Screen visible from 10m behind taxi

### Step 4: Test (5 minutes)
1. Power on tablet (should auto-start app)
2. Verify screen showing content
3. Check admin panel: heartbeat received?
4. Drive 5 minutes, verify GPS updates
5. Upload new image, verify update within 5 min

**Total installation time: ~35 minutes per taxi**

---

## Tools Required

- Screwdriver set
- Wire cutters
- Electrical tape
- Zip ties (100 pack)
- Multimeter (test voltage)
- Drill (if using bolts)

**Total tool cost**: ~$30 (reusable across all installations)

---

## Cost Breakdown (Per Unit)

| Component | Cost (USD) |
|-----------|-----------|
| Android tablet | $80 - $120 |
| Waterproof case | $10 - $15 |
| Power converter | $5 |
| Mounting hardware | $5 |
| 4G SIM card (1 month) | $3 |
| Installation labor | $20 |
| **Total** | **$123 - $168** |

**Average**: ~$145 per taxi for MVP deployment

---

## Production Hardware (Future)

Once validated, custom hardware would cost ~$50-80 per unit at scale:

**Custom Display Unit**:
- Purpose-built Android board (not consumer tablet)
- Smaller form factor
- Better heat management
- Built-in 4G modem
- 5-year lifespan (vs 2-year for tablets)
- Injection-molded weatherproof case
- Professional mounting system

**Manufacturing cost** (10,000 units): ~$50/unit
**Manufacturing cost** (50,000 units): ~$35/unit

But NOT for MVP. Use off-the-shelf parts to validate first.

---

## Risk Mitigation

### Risk: Tablet overheats in sun
**Solution**:
- Use white/reflective case
- Add ventilation holes
- Test during hottest hours
- If fails: upgrade to industrial tablet (~$250)

### Risk: Tablet battery degrades
**Solution**:
- Keep plugged in 24/7 (preserve battery)
- Replace after 12 months
- Budget for 10% replacement rate

### Risk: Water damage
**Solution**:
- Ensure case properly sealed
- Add silicone gasket
- Check seals weekly
- Budget for 5% water damage failures

### Risk: Theft
**Solution**:
- Make case hard to remove quickly
- Mark tablets as "tracking device" (deter theft)
- Budget for 5-10% theft rate
- Add GPS tracking (already in app)

### Risk: Screen not visible in daylight
**Solution**:
- Set brightness to 100%
- Use high-nit display (500+ nits)
- If fails: upgrade to outdoor display (~$300)

---

## Alternative Approaches (NOT for MVP)

### E-Ink Displays
- Pros: Low power, excellent daylight visibility
- Cons: No color, slow refresh, expensive
- Cost: ~$200-400 per unit
- Decision: Skip for MVP, revisit for production

### Roof-Top LED Boards
- Pros: Bright, visible, professional
- Cons: Very expensive ($800-1,500), complex
- Decision: Skip for MVP, consider for Phase 2

### In-Car Displays (Headrest Screens)
- Pros: Captive audience (passengers)
- Cons: Lower impression volume
- Decision: Different product, not testing here

---

## Vendor List (Vietnam)

**Electronics**:
- Phong Vũ (phongvu.vn) - tablets, accessories
- FPT Shop (fptshop.com.vn) - consumer electronics
- Thế Giới Di Động (thegioididong.com) - mobile devices

**Waterproof Cases**:
- Shopee Vietnam (shopee.vn) - search "hộp chống nước"
- Lazada Vietnam (lazada.vn) - generic cases

**SIM Cards**:
- Viettel Store (viettel.com.vn)
- Mobifone Store (mobifone.vn)
- Any convenience store (prepaid SIM widely available)

**Mounting Hardware**:
- Local hardware store (any district in HCMC/Hanoi)

---

## Next Steps

1. **Week 1**: Buy 3 units, install on test taxis
2. **Week 2**: Monitor performance, identify issues
3. **Week 3**: If successful, order 47 more units
4. **Week 4**: Scale to 50 taxis, validate

**Key learning**: Hardware costs, failure rates, operational issues.

This informs production hardware design for 5,000+ unit deployment.
