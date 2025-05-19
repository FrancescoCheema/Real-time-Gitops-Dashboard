
# Real-Time GitOps Dashboard

A fully containerized observability platform for monitoring GitHub push activity in real time. This project leverages **Flask**, **Prometheus**, and **Grafana** to expose and visualize repository events.

---

## Overview

This system listens for GitHub `push` events via webhook, processes them using a lightweight Flask app, and emits metrics such as author, target branch, and timestamp. Prometheus scrapes these metrics, and Grafana visualizes push trends across time and contributors.

---

## Tech Stack

| Tool         | Purpose                                  |
|--------------|-------------------------------------------|
| Flask        | Receives GitHub webhooks and emits metrics |
| Prometheus   | Scrapes `/metrics` and stores time-series data |
| Grafana      | Visualizes data with customizable dashboards |
| Ngrok        | Exposes local webhook listener to GitHub |
| Docker       | Containerizes and orchestrates the stack |

---

## Example Metric

```text
# HELP github_push_total Total GitHub push events
# TYPE github_push_total counter
github_push_total{author="FrancescoCheema", branch="main"} 3
```

---

## Features

- Webhook listener for GitHub push events
- Prometheus-compatible custom metrics
- Grafana dashboard with author/branch insights
- Docker Compose orchestration
- Test route for local metric simulation

---

## Project Structure

```
.
├── webhook-monitor/
│   └── app.py             # Flask app handling webhook and metrics
├── prometheus.yml         # Prometheus config with scrape targets
├── ngrok.yml              # Ngrok config with authtoken and tunnel
├── docker-compose.yml     # Main orchestration file
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 1. Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/real-time-gitops-dashboard.git
cd real-time-gitops-dashboard
```
### OPTIONAL - If you prefer running the app outside of Docker, set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\\Scripts\\activate
pip install -r requirements.txt
python app.py

```

### 2. Configure Ngrok
``` You will need an Ngrok account and an authtoken, you can read the documentation here: https://ngrok.com/docs/getting-started/

Edit `ngrok.yml` with your details:
```yaml
version:
authtoken: "your authtoken" 
tunnels:
  webhook:
    proto: http
    addr: webhook-listener:8080
```

### 3. Launch the Stack

```bash
docker compose up --build
```

### 4. Set Webhook on GitHub

Go to your GitHub repo:  
**Settings → Webhooks → Add Webhook**

Use the public Ngrok URL:
```
https://your-ngrok-url.ngrok-free.app/webhook
```

---

## 5. Grafana

- Access Grafana at: [http://localhost:3000](http://localhost:3000)
- Default credentials: `admin / admin`
- Add Prometheus data source: `http://prometheus:9090`
- Create dashboards using:
  - `github_push_total`
  - `sum by (author)(github_push_total)`
  - `rate(github_push_total[1m])`

---

## 6. Testing Locally

An optional `/test_push` route can simulate a push:

```
GET http://localhost:8080/test_push
```

Useful for validating metrics before connecting GitHub.

---

## 7. Use Cases

- GitOps metrics tracking
- Contributor push frequency analysis
- CI/CD pipeline observability
- Real-time GitHub activity dashboards

---

