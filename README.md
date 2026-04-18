# ⚡ Power Management Backend

A production-structured REST API for ingesting, storing, analysing, and alerting on real-time telemetry from power devices such as solar panels, battery systems, or any IoT-connected power source.

Built with **Django 6**, **Django REST Framework**, and **PostgreSQL**.

---

## Features

- **Real-time ingestion**  accepts device telemetry via HTTP POST
- **Automatic alert engine**  triggers LOW_BATTERY, HIGH_USAGE, and INEFFICIENCY alerts on every reading
- **Query APIs**  device status, reading history, and alert feed
- **Analytics layer**  efficiency percentage, battery drain rate, estimated time remaining
- **Device simulator**  standalone script that mimics a live device sending data
- **Load tested**  verified under continuous 1-second write intervals

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6 + Django REST Framework |
| Database | PostgreSQL |
| Language | Python 3.12 |
| Auth | None (planned: JWT) |

---

## Project Structure

```
power_backend/
├── core/
│   ├── models.py           # Device, PowerReading, Alert
│   ├── serializers.py      # Input validation
│   ├── views.py            # 4 API views
│   ├── urls.py             # Route definitions
│   └── services/
│       ├── alerts.py       # Alert trigger logic
│       └── analytics.py    # Efficiency, drain rate, time remaining
├── power_backend/
│   ├── settings.py
│   └── urls.py
└── simulator.py            # Fake device  sends readings on interval
```

---

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 14+

### 1. Clone & install

```bash
python -m venv .venv
source .venv/bin/activate
pip install django djangorestframework psycopg2-binary
```

### 2. Configure PostgreSQL

```bash
sudo service postgresql start
sudo -u postgres psql
```

```sql
CREATE DATABASE power_db;
CREATE USER power_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE power_db TO power_user;
GRANT ALL ON SCHEMA public TO power_user;
\q
```

### 3. Configure Django

In `power_backend/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'core',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'power_db',
        'USER': 'power_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a device

```bash
python manage.py shell
```

```python
from core.models import Device
d = Device.objects.create(name="Solar Panel 1", location="Rooftop")
print(d.id)  # Copy this UUID
```

### 6. Start the server

```bash
python manage.py runserver
```

### 7. Run the simulator

Update `DEVICE_ID` in `simulator.py` with your device UUID, then:

```bash
python simulator.py
```

---

## API Reference

### POST `/api/readings/`

Ingest a new power reading. Triggers the alert engine automatically.

**Request body:**
```json
{
  "device": "your-device-uuid",
  "battery_level": 80.0,
  "solar_input": 120.0,
  "power_consumption": 90.0
}
```

**Response:**
```json
201 Created
{"status": "reading saved"}
```

---

### GET `/api/devices/{id}/status/`

Latest reading for a device plus computed analytics.

**Response:**
```json
{
  "device": "Solar Panel 1",
  "battery_level": 43.36,
  "solar_input": 95.44,
  "power_consumption": 239.79,
  "timestamp": "2026-04-18T07:27:51Z",
  "efficiency_pct": 39.82,
  "drain_rate_per_interval": -1.24,
  "estimated_minutes_remaining": 17.6
}
```

---

### GET `/api/devices/{id}/history/`

Last 50 readings, newest first.

```json
[
  {
    "battery_level": 43.36,
    "solar_input": 95.44,
    "power_consumption": 239.79,
    "timestamp": "2026-04-18T07:27:51Z"
  }
]
```

---

### GET `/api/devices/{id}/alerts/`

Last 20 alerts, newest first.

```json
[
  {
    "alert_type": "HIGH_USAGE",
    "message": "High power consumption detected: 239.79W",
    "resolved": false,
    "created_at": "2026-04-18T07:27:51Z"
  }
]
```

---

## Alert Engine

Alerts are generated automatically after each ingested reading based on these rules:

| Alert Type | Trigger |
|---|---|
| `LOW_BATTERY` | `battery_level < 20%` |
| `HIGH_USAGE` | `power_consumption > 150W` |
| `INEFFICIENCY` | `consumption / solar_input > 1.5` |

---

## Analytics

Three functions computed on the status endpoint:

| Metric | Formula |
|---|---|
| `efficiency_pct` | `(solar_input / power_consumption) × 100` |
| `drain_rate_per_interval` | Average battery drop across last 10 readings |
| `estimated_minutes_remaining` | `(battery / drain_rate) × interval / 60` |

---

## Known Limitations

- **No authentication**  all endpoints are public
- **No alert deduplication**  a LOW_BATTERY alert fires every reading while condition holds
- **No pagination**  history capped at 50, alerts at 20
- **No input range validation**  battery_level could accept values outside 0–100

---

## Roadmap

- [ ] JWT authentication (djangorestframework-simplejwt)
- [ ] Alert cooldown / deduplication logic
- [ ] Pagination on history and alerts endpoints
- [ ] PATCH `/api/devices/{id}/alerts/{id}/` to resolve alerts
- [ ] pytest-django test suite
- [ ] Multi-device simulator
- [ ] DB indexes on (device_id, timestamp) for query performance

---

## License

MIT
