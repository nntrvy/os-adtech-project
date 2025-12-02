# Building a Core Backend for an In-Taxi Ad Platform

This document outlines the concepts, architecture, and a step-by-step plan to build a robust backend for an in-taxi ad distribution and tracking platform. The system is designed to serve ads to digital screens in vehicles, using trip data for targeting.

---

## 1. Core Concepts

First, let's define the "nouns" of our system. These are the fundamental entities we will be modeling.

- **Advertiser**: The entity that owns campaigns. An advertiser has a budget and one or more campaigns.
- **Campaign**: A specific advertising objective. It has a total budget, a start and end date, and targeting rules. (e.g., "Nike's Holiday Shoe Promotion").
- **Ad Creative**: The actual content to be displayed. This could be an image, a video, or rich HTML. Each creative belongs to a campaign and has properties like its URL, format, and a destination URL for clicks.
- **Placement**: A specific digital screen in a specific vehicle. We need to identify each screen uniquely.
- **Trip Data**: Real-time information sent from the taxi with each ad request. This is our primary targeting vector. It should include:
    - Pickup location (latitude, longitude)
    - Drop-off location (latitude, longitude)
    - Current time
    - Vehicle ID / Placement ID
- **Impression**: A record of a single ad creative being successfully displayed on a placement.
- **Interaction (e.g., Click)**: A record of a user interacting with the ad, typically by tapping the screen.

---

## 2. System Architecture

A microservices architecture is a good fit here to separate concerns and allow for independent scaling of different system parts.

![System Architecture Diagram](httpsa://i.imgur.com/3yYvV3c.png)

1.  **Ad Management Service (The "Office")**
    - **Purpose**: Provides a web interface or API for advertisers to create and manage their campaigns and upload ad creatives.
    - **Operations**: Standard CRUD (Create, Read, Update, Delete) for advertisers, campaigns, and creatives.
    - **Technology**: A standard web framework (e.g., Python/Django, Node/Express) with a persistent relational database.

2.  **Ad Selection Service (The "Ad Server")**
    - **Purpose**: This is the brain. It receives a request from a taxi screen (with trip data) and decides which ad to show.
    - **Operations**:
        1.  Filters all available campaigns based on the incoming trip data (location, time, etc.).
        2.  Ranks the eligible ads (if more than one matches).
        3.  Returns a single ad creative to be displayed.
    - **Constraints**: Must be **fast** (low latency) and **highly available**.
    - **Technology**: A high-performance framework (Python/FastAPI, Go). It needs fast access to campaign data, often via a cache (like Redis).

3.  **Event Tracking Service (The "Collector")**
    - **Purpose**: To ingest a massive volume of events (impressions, clicks) from all active taxis.
    - **Operations**: Provides simple, highly available endpoints to receive tracking pings.
    - **Constraints**: Must handle very high write throughput.
    - **Technology**: This service should be simple. It takes the event data and immediately pushes it into a message queue (like **Apache Kafka** or **RabbitMQ**). This decouples ingestion from processing.

4.  **Data & Analytics Pipeline**
    - **Purpose**: To process the raw event data from the message queue, aggregate it, and update campaign performance metrics (e.g., impressions delivered, budget spent).
    - **Technology**: A stream or batch processing system (e.g., Spark, Flink, or simple Python workers) reads from Kafka, transforms the data, and writes it to an analytical database or updates the main PostgreSQL database.

### Database Choices:
-   **Primary Database (PostgreSQL)**: Excellent for the structured, relational data of the Ad Management service (campaigns, advertisers, ad metadata). Its **PostGIS** extension is critical for efficient geospatial queries (e.g., "is this trip's start point inside this campaign's target area?").
-   **Cache (Redis)**: Used by the Ad Selection service to store active campaign and targeting data in memory. Reading from Redis is much faster than from PostgreSQL, which is crucial for low-latency ad serving.
-   **Message Queue (Kafka)**: Acts as a buffer for the high volume of tracking events, ensuring we never lose an impression record even if the backend processing is slow.

---

## 3. API Endpoints

Here are the critical API endpoints that the services will expose.

### Ad Selection Service

#### `POST /v1/ads/select`
This is the main endpoint called by the taxi's screen every time it needs a new ad.

**Request Body:**
```json
{
  "placementId": "taxi-042-screen-1",
  "trip": {
    "pickup": { "lat": 10.7769, "lon": 106.7009 }, // Ho Chi Minh City
    "dropoff": { "lat": 10.8231, "lon": 106.6297 }
  },
  "timestamp": "2025-12-02T10:00:00Z"
}
```

**Success Response (200 OK):**
```json
{
  "impressionId": "imp_random_uuid_string",
  "creative": {
    "id": "creative_123",
    "type": "video/mp4",
    "assetUrl": "https://cdn.example.com/videos/nike-ad-15s.mp4",
    "clickUrl": "https://ad-backend.com/v1/track/click/creative_123"
  }
}
```

### Event Tracking Service

#### `POST /v1/track/impression`
Called by the taxi screen *after* the ad has been successfully displayed for a minimum duration. This is a "fire-and-forget" request.

**Request Body:**
```json
{
  "impressionId": "imp_random_uuid_string" 
}
```
**Response**: `202 Accepted` - The service acknowledges receipt and will process it.

#### `GET /v1/track/click/{impressionId}`
When a user taps the ad, the taxi screen opens a web view to this URL. This service records the click and then immediately redirects the user to the advertiser's actual destination URL.

**Response**: `302 Found` with a `Location` header pointing to the ad's `destinationUrl`.

---

## 4. Ad Selection Logic (Step-by-Step)

This is the core logic inside the `POST /v1/ads/select` endpoint.

1.  **Generate Impression ID**: Create a unique ID for this potential ad view. This ID is returned to the client and used for subsequent tracking.
2.  **Fetch Candidate Campaigns**: Get all campaigns that are currently `active` and have a budget > 0. This list should be heavily cached in Redis and updated only when campaigns are changed in the Management Service.
3.  **Filter by Targeting Rules**: For each candidate campaign, check its targeting rules against the `trip` data from the request. A campaign is eliminated if *any* of its rules don't match.
    - **Date/Time Rule**: Is the current day/time within the campaign's schedule? (e.g., "weekdays 8am-10am").
    - **Geofence Rule**: Is the `trip.pickup.lat/lon` inside the campaign's target geographic area? This is where a **PostGIS `ST_Contains`** query is powerful and efficient.
    - **Other Trip Rules**: You could add rules for trip duration, drop-off area, etc.
4.  **Rank Eligible Ads**: If multiple campaigns pass the filtering stage, you need a strategy to pick one.
    - **Simple Start**: Pick one randomly. This is fair and easy to implement.
    - **Advanced**: Implement a ranking model. A common one is to rank by **eCPM (effective Cost Per Mille)**, which is calculated as `(Bid Price * Click-Through-Rate) * 1000`. This requires historical performance data.
5.  **Return the Winner**: Select the top-ranked ad creative.
6.  **Pre-decrement Budget (Optional)**: You can tentatively decrement the winning campaign's budget to reserve it. This prevents over-spending but adds complexity. The final decrement happens after the impression is confirmed.

---

## 5. Implementation Plan (MVP)

Let's build the simplest possible version using **Python (FastAPI)** and **PostgreSQL**.

**Phase 1: Setup & Management API**
1.  **Initialize Project**: Set up a Python environment and install libraries:
    ```bash
    pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary geoalchemy2
    ```
2.  **Define Data Models**: Use SQLAlchemy to create Python classes that map to your database tables (`Campaign`, `AdCreative`, etc.). Use GeoAlchemy2 for location fields.
3.  **Build Management API**: Create simple FastAPI endpoints for CRUD operations on your models. This will allow you to seed the database with test campaigns.

**Phase 2: Ad Selection & Tracking MVP**
4.  **Create `/v1/ads/select` Endpoint**:
    - Implement the logic to fetch all campaigns from the database.
    - Start with simple filtering: check if the campaign is active and within its `start_date` and `end_date`.
    - Randomly select one of the matching campaigns.
    - Return the associated ad creative.
5.  **Create `/v1/track/impression` Endpoint**:
    - This endpoint will receive an `impressionId`.
    - For the MVP, it can simply log the ID to the console or a file. In a real system, this writes to a database table.

**Phase 3: Adding Geo-Targeting**
6.  **Add Geo-Data**: Add a `geography` column to your `Campaigns` table using `GeoAlchemy2`. Write a script to populate it with a sample polygon (e.g., a district in a city).
7.  **Implement Geo-Filter**: Update the `/v1/ads/select` logic to include a PostGIS query that filters campaigns where the `trip.pickup` location is contained within the campaign's target geography.

**Phase 4: Scaling & Budgeting**
8.  **Budget Management**: Add a `budget` column to campaigns. Decrement the budget after a successful impression is tracked. The ad selection logic should filter out campaigns with no budget.
9.  **Introduce Caching**: Integrate Redis. Before querying the database for campaigns, check Redis first.
10. **Decouple Tracking**: For handling high volumes, modify the tracking service to write events to a message queue like Kafka instead of directly to the database. Create a separate worker process to read from the queue and update the database in batches.
