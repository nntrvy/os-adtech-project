# How Grab Built Their Scalable Ad Server

**Source:** [Grab Engineering Blog - Scalable Ad Server](https://engineering.grab.com/scalable-ads-server)
**Created:** 2025-12-03
**Purpose:** Engineering reference for building scalable ad serving systems

---

## Executive Summary

Grab built a unified, microservices-based ad serving platform that handles multiple ad formats across all their app surfaces. The system prioritizes low latency, graceful degradation, and global optimization while supporting sophisticated targeting, pacing, and auction mechanisms.

**Key Metrics & Requirements:**
- Strict latency limits for ad serving flow
- High availability with graceful degradation
- Support for multiple ad formats (image, video, search, rewarded)
- Cross-platform serving (home, ride booking, food search, etc.)

---

## System Architecture

### Seven-Stage Ad Serving Pipeline

The ad server operates as a sequential pipeline with seven distinct stages:

```
Request → Targeting → Capping → Pacing → Scoring → Ranking → Pricing → Response
                                                                    ↓
                                                                Tracking
```

#### 1. Targeting Stage
**Purpose:** Filter ads relevant to the current request context

**Implementation:**
- **Data Store:** ElasticSearch
- **Query Against:**
  - Search keywords
  - User location
  - Time of day
  - User preferences
  - Other targeting criteria

**Why ElasticSearch?**
- Multi-criteria querying capability
- Flexible schema for diverse targeting rules
- Fast full-text search performance

**Key Insight:** ElasticSearch serves as the "ads repository" - all available ads live here with their targeting criteria attached.

---

#### 2. Capping Stage
**Purpose:** Enforce budget and frequency limits

**Implementation:**
- **Data Store:** ScyllaDB (campaign statistics)
- **Filters:**
  - Ads that exceeded daily/total budget
  - Ads that hit frequency caps (max impressions per user)
- **Operation:** Read current spend/impression counts and filter accordingly

**Key Insight:** Capping is a hard filter - ads that violate caps are completely removed from consideration.

---

#### 3. Pacing Stage
**Purpose:** Distribute budget evenly throughout the day

**Implementation:**
- **Data Store:** ScyllaDB (impression tracking)
- **Logic:** Adjusts ad serving probability based on current spend rate vs. target
- **Example:** If a campaign has spent 30% of budget by noon, reduce serving probability to stretch remaining budget

**Key Insight:** Unlike capping (binary filter), pacing is probabilistic - ads can still serve but with adjusted frequency.

---

#### 4. Scoring Stage
**Purpose:** Calculate relevance score for each ad candidate

**Scoring Formula:**
```
Score = f(pCTR, pCVR, heuristics)
```

**Components:**
- **pCTR:** Predicted click-through rate (ML model)
- **pCVR:** Predicted conversion rate (ML model)
- **Heuristics:** Rule-based adjustments

**Key Insight:** Scoring is where ML models influence ad selection. Models predict user behavior to optimize for business outcomes.

---

#### 5. Ranking Stage
**Purpose:** Order ads for final selection

**Implementation:**
- **Algorithms Supported:**
  - Lottery-based (probability weighted)
  - Auction-based (highest bid wins)
  - Configurable per campaign type
- **Inputs:** Scores from previous stage + bid prices
- **Output:** Ordered list of ads

**Key Insight:** Ranking integrates ML predictions with auction economics to balance relevance and revenue.

---

#### 6. Pricing Stage
**Purpose:** Determine clearing price for each ad impression

**Implementation:**
- **Mechanisms:** Auction-based pricing (e.g., second-price auction)
- **Billing Models Supported:**
  - CPM (cost per mille/impression)
  - CPC (cost per click)
  - CPA (cost per acquisition/purchase)

**Key Insight:** Decoupling ranking from pricing allows for sophisticated auction mechanisms while supporting multiple billing models.

---

#### 7. Tracking Stage
**Purpose:** Close the feedback loop for optimization

**Implementation:**
- **Data Collection:**
  - API calls (synchronous events)
  - Kafka streams (real-time event pipeline)
  - Batch data pipelines (delayed conversions)
- **Data Destination:** ScyllaDB (statistics store)
- **Events Tracked:**
  - Impressions
  - Clicks
  - Conversions/purchases
  - User interactions

**Key Insight:** Tracking feeds back into Capping, Pacing, and ML model training - creating a closed optimization loop.

---

## Technology Stack Decisions

### ElasticSearch (Ad Repository)

**Use Case:** Store and query all available ads with targeting criteria

**Why Chosen:**
- Excellent multi-criteria query performance
- Flexible schema for diverse targeting rules
- Full-text search for keyword targeting
- Horizontal scalability

**Trade-offs:**
- Requires extensive tuning for latency optimization
- More complex than simple key-value stores

---

### ScyllaDB (Statistics Store)

**Use Case:** Store campaign statistics, spend tracking, impression counts

**Why Chosen:**
- "Scalable, cost-effective"
- Handles high read/write volume
- Low latency for real-time lookups
- Compatible with Cassandra ecosystem

**Alternative Considered:**
- Redis (too expensive at scale)
- Cassandra (ScyllaDB offers better performance)

**Trade-offs:**
- Eventual consistency model
- Requires careful data modeling for query patterns

---

### Kafka (Event Streaming)

**Use Case:** Real-time data pipeline for tracking events

**Why Chosen:**
- Industry standard for event streaming
- Decouples ad server from downstream analytics
- Supports high throughput
- Reliable delivery guarantees

**Trade-offs:**
- Operational complexity
- Requires separate consumer infrastructure

---

## Core Design Principles

### 1. Latency Optimization

**Requirement:** Strict limits on latency of ad serving flow

**Strategies:**
- Extensive ElasticSearch tuning
- Parallelized serving steps wherever possible
- A/B tested all changes for performance impact
- Strict timeouts on all dependency calls

**Why Critical:** Ad serving happens in the hot path of user experience. Every millisecond matters.

---

### 2. Graceful Degradation

**Requirement:** Never serve nothing due to failures

**Implementation:**
- Strict timeouts on dependency calls (ElasticSearch, ScyllaDB)
- Fallback to non-personalized results during failures
- Prioritizes availability over optimization

**Philosophy:** "Better to show a generic ad than no ad at all"

**Example Flow:**
```
1. Try personalized targeting (ElasticSearch)
2. If timeout → Fall back to location-only targeting
3. If still failing → Serve default ads for region
4. Always serve something
```

---

### 3. Global Optimization

**Requirement:** Unified system across all ad types and surfaces

**Implementation:**
- Single ad server for all formats (image, video, search, rewarded)
- Supports all app surfaces (home, ride booking, food search)
- Shared infrastructure and optimization improvements

**Benefits:**
- Cross-platform efficiency improvements
- Unified ML model training
- Simplified operations
- Better resource utilization

**Trade-off:** More complex system, but economies of scale justify it.

---

## Performance Optimization Patterns

### Pattern 1: Parallel Stage Execution

**Problem:** Sequential pipeline adds latency

**Solution:** Parallelize independent stages where possible

**Example:**
```
# Sequential (slower)
targeting → capping → pacing → scoring

# Parallel (faster)
targeting → [capping + pacing] → scoring
```

**Caveat:** Only parallelize stages that don't depend on each other's output.

---

### Pattern 2: Timeout-Based Degradation

**Problem:** Slow dependencies block entire request

**Solution:** Set aggressive timeouts, fall back gracefully

**Implementation:**
```
try:
    ads = elasticsearch.query(criteria, timeout=50ms)
except TimeoutError:
    ads = elasticsearch.query(simple_criteria, timeout=30ms)
except TimeoutError:
    ads = get_default_ads_for_region()
```

**Key Metric:** P99 latency should never exceed acceptable threshold.

---

### Pattern 3: Read-Optimized Data Modeling

**Problem:** ScyllaDB writes are fast, but read patterns matter

**Solution:** Denormalize data for read patterns

**Example:**
```
# Instead of joining tables, store pre-aggregated stats:
campaign_stats {
    campaign_id: UUID
    date: Date
    total_impressions: Counter
    total_spend: Decimal
    hourly_impressions: Map<Hour, Counter>
}
```

**Trade-off:** Increased write complexity for faster reads.

---

## ML Integration Strategy

### Prediction Models

**pCTR (Predicted Click-Through Rate):**
- Features: User demographics, location, time, historical behavior
- Update frequency: Daily retraining
- Serving: Real-time inference during Scoring stage

**pCVR (Predicted Conversion Rate):**
- Features: User purchase history, app usage patterns, session context
- Update frequency: Daily retraining
- Serving: Real-time inference during Scoring stage

**Key Insight:** Models are called in the Scoring stage, not earlier - this keeps Targeting stage fast and simple.

---

### Feedback Loop Architecture

```
Ad Impression → Tracking → Kafka → Data Pipeline → Training Data → ML Models
                                                                        ↓
                                                            Updated pCTR/pCVR
```

**Latency:** Hours to days for model updates (batch training)

**Future Goal:** "Real-time ML-driven personalization" for faster feedback loops.

---

## Auction Mechanism Design

### Ranking Algorithm

**Input:**
- Ad scores (from Scoring stage)
- Advertiser bids

**Output:**
- Ranked list of ads

**Algorithm Options:**
1. **Pure Auction:** Highest bid wins
2. **Hybrid:** `score * bid` determines rank
3. **Lottery:** Probabilistic selection weighted by `score * bid`

**Grab's Approach:** Configurable per campaign type for flexibility.

---

### Pricing Algorithm

**Second-Price Auction:**
- Winner pays price of second-highest bid + $0.01
- Encourages truthful bidding
- Industry standard for ad auctions

**Why Separate from Ranking?**
- Allows complex ranking without complicating pricing
- Supports multiple billing models (CPM, CPC, CPA)

---

## Scaling Strategies

### Horizontal Scaling

**ElasticSearch:**
- Shard by ad category or region
- Replicas for read throughput

**ScyllaDB:**
- Partition by campaign_id or user_id
- Replication factor = 3 for durability

**Ad Server Instances:**
- Stateless service
- Load balancer distributes requests
- Auto-scaling based on traffic

---

### Data Pipeline Scaling

**Kafka:**
- Partition by user_id or campaign_id
- Separate topics for impressions, clicks, conversions

**Stream Processing:**
- Flink or Spark Streaming for aggregations
- Micro-batching for efficiency

---

## Lessons Learned & Future Improvements

### Identified Priorities

1. **Real-time ML Personalization**
   - Current: Batch model updates (hours/days lag)
   - Goal: Online learning for instant personalization
   - Challenge: Inference latency vs. model complexity

2. **Auction Strategy Refinement**
   - Current: Basic second-price auction
   - Goal: "Marketplace efficiency" improvements
   - Ideas: Reserve prices, bid shading, multi-item auctions

3. **New Ad Format Expansion**
   - Current: Image, video, search, rewarded
   - Future: "As Grab's service portfolio grows"
   - Challenge: Unified serving for diverse formats

4. **Continued Latency Improvements**
   - Current: "Strict limits" enforced
   - Goal: "Latency and reliability improvements at scale"
   - Approach: Ongoing optimization and A/B testing

---

## Key Takeaways for Our Implementation

### What to Copy

✅ **Seven-stage pipeline architecture**
- Clean separation of concerns
- Easy to test and optimize each stage independently

✅ **ElasticSearch for ad targeting**
- Proven at scale
- Flexible targeting criteria

✅ **ScyllaDB for statistics**
- Cost-effective for high write volume
- Good read performance

✅ **Graceful degradation pattern**
- Critical for production reliability
- Timeouts + fallbacks = always serve something

✅ **A/B testing discipline**
- Validate every performance change
- Data-driven optimization

---

### What to Adapt for Vietnam Taxi DOOH

🔧 **Simplify Initial ML Models**
- Start with simpler heuristics
- Add pCTR/pCVR when we have enough data

🔧 **Consider Simpler Statistics Store**
- Redis + PostgreSQL might be sufficient initially
- ScyllaDB when we hit scale limits

🔧 **Auction Later, Fixed Pricing First**
- Start with CPM/CPC fixed rates
- Add auctions once we have multiple competing advertisers

🔧 **Skip Pacing Initially**
- Useful for self-serve platforms
- Manual IO campaigns don't need sophisticated pacing

---

### Critical Questions to Answer

❓ **What's our latency budget?**
- Grab has "strict limits" - what are ours?
- DOOH content updates: seconds okay vs. milliseconds

❓ **Do we need real-time stats?**
- Grab uses ScyllaDB for real-time capping/pacing
- DOOH campaigns: hourly updates might be sufficient

❓ **How many ads per request?**
- Mobile app: 1-5 ads per screen
- Taxi screen: 1 ad at a time, but multiple screens per fleet

❓ **Self-serve vs. Managed IO?**
- Self-serve needs capping, pacing, auctions
- Managed IO can start simpler

---

## Implementation Checklist

### Phase 1: MVP (Targeting + Basic Serving)
- [ ] ElasticSearch cluster for ad repository
- [ ] Targeting stage implementation
- [ ] Basic scoring (rule-based, no ML)
- [ ] Simple ranking (round-robin or weighted random)
- [ ] Tracking via Kafka
- [ ] PostgreSQL for campaign stats

### Phase 2: Optimization (Pacing + Capping)
- [ ] Migrate stats to Redis or ScyllaDB
- [ ] Implement capping stage
- [ ] Implement pacing stage
- [ ] Add graceful degradation patterns
- [ ] Performance testing + optimization

### Phase 3: Intelligence (ML + Auctions)
- [ ] Build pCTR/pCVR models
- [ ] Integrate ML into scoring stage
- [ ] Implement auction mechanisms
- [ ] Add second-price pricing
- [ ] Real-time feedback loop optimization

---

## References

- **Source Article:** https://engineering.grab.com/scalable-ads-server
- **Related Technologies:**
  - ElasticSearch: https://www.elastic.co/
  - ScyllaDB: https://www.scylladb.com/
  - Apache Kafka: https://kafka.apache.org/

- **Related Concepts:**
  - Second-price auctions (Vickrey auctions)
  - Ad pacing algorithms
  - Real-time bidding (RTB) systems
  - Programmatic advertising architecture

---

**Document Status:** Initial version based on Grab engineering blog
**Last Updated:** 2025-12-03
**Recommended Review Frequency:** Update as we implement and learn
