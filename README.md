This project exhibits the implementation of an observability stack for a containerized web app, showing SRE practices like metrics collection, monitoring, and alerting.

**Technologies Used:** Python Flask, Docker, Prometheus, Grafana, Telegram Bot API  
**Project Duration:** 4 weeks  
**Objective:** Build end-to-end monitoring and observability for a simple web application


## Project Architecture

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │────│   Prometheus    │────│    Grafana      │
│   (Port 5000)   │    │   (Port 9090)   │    │   (Port 3000)   │
│                 │    │                 │    │                 │
│ /metrics        │    │ Scrapes metrics │    │ Visualizes data │
│ /health         │    │ every 5s        │    │ Creates alerts  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Telegram Bot   │
                                               │  Alert Delivery │
                                               └─────────────────┘

## Application Development

### Flask Web Application

The core application is a simple portfolio website built with Python Flask framework, instrumented with Prometheus metrics for observability.

**File Structure:**
```
portfolio-sre/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
├── Dockerfile
├── prometheus.yml
└── README.md
```
```
**Key Features:**
- **Health Check Endpoint:** `/health` - Returns application status for monitoring
- **Metrics Endpoint:** `/metrics` - Exposes Prometheus-formatted metrics
- **Request Instrumentation:** Tracks total requests and response times
- **Simulated Processing:** Random delays to demonstrate response time monitoring

```

## Containerization

**Container Build Process:**

# Build the Docker image
docker build -t my-portfolio .

# Run the containerized application
docker run -p 5000:5000 my-portfolio
```

## Monitoring Infrastructure Setup

### Prometheus Configuration

Since Prometheus was already installed on the system, the existing installation was leveraged and configured to scrape metrics from the containerized application.

**Prometheus Configuration Update:**
Added the following job to the existing `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'portfolio-app'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

**Metrics Collected:**
- `app_requests_total` - Counter tracking total HTTP requests by method and endpoint
- `app_request_duration_seconds` - Histogram measuring request processing time
- Default Python runtime metrics (memory, GC, process stats)

**Prometheus Restart:**
```bash
sudo systemctl restart prometheus
```

**Verification:**
- Prometheus UI accessible at `http://localhost:9090`
- Target status confirmed as "UP" in Status → Targets
- Metrics queryable via PromQL

---

## Data Visualization with Grafana

### Grafana Integration

Leveraged existing Grafana installation running on port 3000. Connected Grafana to Prometheus data source and created comprehensive monitoring dashboards.

**Data Source Configuration:**
- **Type:** Prometheus
- **URL:** `http://localhost:9090`
- **Access:** Server (default)

### Dashboard Creation

Created a custom dashboard with multiple panels to visualize application performance:

**Panel 1: Total Page Visits**
- **Query:** `app_requests_total`
- **Visualization:** Stat
- **Purpose:** Shows cumulative request count

**Panel 2: Request Rate**
- **Query:** `rate(app_requests_total[1m]) * 60`
- **Visualization:** Time series
- **Purpose:** Real-time requests per minute

**Panel 3: Average Response Time**
- **Query:** `rate(app_request_duration_seconds_sum[1m]) / rate(app_request_duration_seconds_count[1m])`
- **Visualization:** Stat
- **Purpose:** Application performance monitoring

**Panel 4: Response Time Distribution**
- **Query:** `histogram_quantile(0.95, rate(app_request_duration_seconds_bucket[5m]))`
- **Visualization:** Time series
- **Purpose:** 95th percentile response time tracking

---

## Alerting Implementation

### Telegram Bot Integration

Implemented Telegram-based alerting for real-time notification delivery, chosen for its simplicity and reliability.

**Bot Setup Process:**
1. Created bot via @BotFather on Telegram
2. Obtained bot token: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
3. Retrieved chat ID through API call
4. Configured Grafana contact point

**Grafana Alert Configuration:**
- **Contact Point Type:** Telegram
- **Bot Token:** [Bot token from BotFather]
- **Chat ID:** [Personal chat ID]

**Alert Rules Implemented:**
1. **Application Down Alert**
   - **Condition:** `rate(app_requests_total[1m]) < 0.01`
   - **Duration:** 1 minute
   - **Action:** Send Telegram notification

2. **High Response Time Alert**
   - **Condition:** `rate(app_request_duration_seconds_sum[1m]) / rate(app_request_duration_seconds_count[1m]) > 0.5`
   - **Duration:** 30 seconds
   - **Action:** Send Telegram notification

---

## Testing and Validation

### Load Testing

Generated traffic to validate monitoring stack functionality:

```bash
# Automated traffic generation
for i in {1..50}; do 
    curl http://localhost:5000
    sleep 2
done
```

### Alert Testing

**Downtime Simulation:**
```bash
# Stop application to trigger alert
docker stop <container-name>

# Verify alert received via Telegram
# Restart application
docker start <container-name>

# Verify recovery notification
```

---

## Key Metrics and KPIs

### Service Level Indicators (SLIs)

**Availability SLI:**
- **Metric:** `up{job="portfolio-app"}`
- **Target:** > 99.9% uptime

**Latency SLI:**
- **Metric:** `histogram_quantile(0.95, rate(app_request_duration_seconds_bucket[5m]))`
- **Target:** < 500ms for 95th percentile

**Throughput SLI:**
- **Metric:** `rate(app_requests_total[5m])`
- **Baseline:** Established through monitoring

### Dashboard Performance

- **Real-time Updates:** 5-second refresh interval
- **Historical Data:** 30-day retention
- **Query Performance:** < 100ms average response time

---

## Lessons Learned

### Technical Insights

1. **Metrics Design:** Counter and histogram metrics provide comprehensive application insight
2. **Container Networking:** Docker host networking simplifies Prometheus scraping configuration
3. **Alert Fatigue:** Careful threshold tuning prevents notification overload
4. **Dashboard Design:** Focus on actionable metrics rather than vanity metrics

### SRE Practices Applied

1. **Observability:** Comprehensive instrumentation from application inception
2. **Monitoring as Code:** Configuration files enable reproducible infrastructure
3. **Incident Response:** Automated alerting reduces mean time to detection (MTTD)
4. **Documentation:** This report enables knowledge transfer and troubleshooting


## Appendix

### Useful Commands

**Application Management:**
```bash
# Build and run application
docker build -t my-portfolio .
docker run -p 5000:5000 my-portfolio

# Check application health
curl http://localhost:5000/health

# View metrics
curl http://localhost:5000/metrics
```

**Monitoring Stack:**
```bash
# Prometheus status
systemctl status prometheus

# Grafana access
http://localhost:3000

# Generate test traffic
for i in {1..20}; do curl http://localhost:5000; sleep 1; done
```

### Repository Structure
```
portfolio-sre/
├── app/
│   ├── app.py              # Main application code
│   ├── requirements.txt    # Python dependencies
│   └── templates/
│       └── index.html      # HTML template
├── Dockerfile              # Container definition
├── prometheus.yml          # Monitoring configuration
├── README.md              # Project documentation
└── docs/
    └── project-report.md   # This technical report
```

--
