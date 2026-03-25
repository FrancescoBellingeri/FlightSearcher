from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "WARNING").upper(), logging.WARNING),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

from flight_search import search_flight

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS") or "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchParams(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_month: str
    start_day: int
    trip_duration: int
    weekend_requirement: str
    times: Optional[str] = None
    stop_number: Optional[int] = None

@app.get('/airports')
async def search_airports(q: str):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                'https://api.skypicker.com/locations',
                params={'term': q, 'locale': 'en-US', 'active_only': 'true', 'limit': 10}
            )
            data = resp.json()

        results = []
        for loc in data.get('locations', []):
            if loc['type'] == 'city':
                results.append({
                    'value': loc['slug'],
                    'label': f"{loc['name']}, {loc['country']['name']}",
                    'type': 'city',
                    'iata': loc.get('code', ''),
                    'city': loc['name'],
                    'airport': '',
                    'country': loc['country']['name'],
                })
            elif loc['type'] == 'airport':
                results.append({
                    'value': loc['code'],
                    'label': f"{loc.get('city', {}).get('name', loc['name'])} - {loc['name']}",
                    'type': 'airport',
                    'iata': loc.get('code', ''),
                    'city': loc.get('city', {}).get('name', loc['name']),
                    'airport': loc['name'],
                    'country': loc.get('country', {}).get('name', ''),
                })

        return {'status': 'OK', 'results': results}
    except Exception as e:
        return {'status': 'Error', 'message': str(e)}


@app.websocket('/ws/search')
async def ws_search(websocket: WebSocket):
    await websocket.accept()
    try:
        params = await websocket.receive_json()
        async for message in search_flight(params):
            await websocket.send_json(message)
    except WebSocketDisconnect:
        logger.info("Client disconnected during search")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
