from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

from flight_search import search_flight

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origin
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


@app.post('/search')
async def start_search(params: SearchParams):
    try:
        result = await search_flight(params.dict())
        return {"status": "OK", "results": result}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
