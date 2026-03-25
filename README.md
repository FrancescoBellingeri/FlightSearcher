# ✈️ FlightSearcher

FlightSearcher is a web application for automated low-cost flight search. It scans an entire month day by day, intercepting Kiwi.com's GraphQL responses via Playwright, and returns the **best** and **cheapest** round-trip option for each departure date — sorted by price.

## Features

- **Airport autocomplete** — searches airports and cities in real time via Kiwi's public API
- **Full-month scan** — iterates every day of the selected month starting from a configurable day
- **Weekend filter** — none / at least one day / full weekend (Sat + Sun)
- **Time filter** — restrict outbound and return departure hours
- **Stop filter** — direct, max 1 stop, max 2 stops, or any
- **Modern UI** — responsive Vue.js + Tailwind CSS frontend

## Tech Stack

| Layer    | Technology                              |
|----------|-----------------------------------------|
| Backend  | Python 3.12, FastAPI, Playwright (rebrowser) |
| Frontend | Node 20, Vue 3, Vite, Tailwind CSS      |
| Scraping | Chromium (headless) via rebrowser-playwright |

---

## 🐳 Quick Start with Docker (recommended)

> Requires [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

```bash
git clone <repository-url>
cd FlightSearcher
docker compose up --build
```

| Service  | URL                    |
|----------|------------------------|
| Frontend | http://localhost:5173  |
| Backend  | http://localhost:8000  |

To stop:
```bash
docker compose down
```

---

## 🛠️ Manual Setup (without Docker)

### Prerequisites

- Python **3.12**
- Node.js **20.20.1**

---

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install --no-cache-dir -r requirements.txt
python -m rebrowser_playwright install chromium
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

> **Note:** Playwright downloads Chromium on first install (~150 MB). This only happens once.

---

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## API Endpoints

| Method | Path       | Description                              |
|--------|------------|------------------------------------------|
| GET    | `/airports?q=<term>` | Autocomplete airports and cities |
| POST   | `/search`  | Run a full-month flight search           |

### POST `/search` — request body

```json
{
  "departure_airport": "milan-italy",
  "arrival_airport": "london-united-kingdom",
  "departure_month": "2026-06",
  "start_day": 1,
  "trip_duration": 3,
  "weekend_requirement": "full",
  "times": "6-22-0-24_6-22-0-24",
  "stop_number": 0
}
```

| Field                | Type    | Values                          |
|---------------------|---------|---------------------------------|
| `departure_airport` | string  | Kiwi city slug or IATA code     |
| `arrival_airport`   | string  | Kiwi city slug or IATA code     |
| `departure_month`   | string  | `YYYY-MM`                       |
| `start_day`         | int     | Day of month to start from      |
| `trip_duration`     | int     | Number of days                  |
| `weekend_requirement` | string | `none` \| `one` \| `full`      |
| `times`             | string  | `out_from-out_to-0-24_ret_from-ret_to-0-24` (optional) |
| `stop_number`       | int     | `0`, `1`, `2`, or `null` for any (optional) |

---

## Project Structure

```
FlightSearcher/
├── backend/
│   ├── app.py              # FastAPI app, endpoints
│   ├── flight_search.py    # Playwright scraping logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.vue                      # Main page and form
│   │   └── components/
│   │       ├── AirportInput.vue         # Autocomplete input
│   │       └── FlightCard.vue           # Flight result card
│   └── Dockerfile
└── docker-compose.yml
```

---

## License

This project is the property of Francesco Bellingeri.
