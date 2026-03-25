from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from flight_search import search_flight

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione, specifica l'origine esatta
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

@app.post('/search')
async def start_search(params: SearchParams):
    try:
        # FastAPI gestisce già il loop asincrono. 
        # Basta 'attendere' il risultato della tua funzione.
        print(params.dict())
        result = await search_flight(params.dict())
        return {"status": "OK", "results": result}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)