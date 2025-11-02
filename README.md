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


**Monitoring Stack:**
```bash
# Prometheus status
systemctl status prometheus

# Grafana access
http://localhost:3000

# Generate test traffic
for i in {1..20}; do curl http://localhost:5000; sleep 1; done
```




