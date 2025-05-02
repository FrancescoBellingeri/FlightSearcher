import threading
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio

from flight_search import search_flight

app = FastAPI()

class SearchParams(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_month: str
    start_day: int
    trip_duration: int
    weekend_requirement: str

@app.post('/search')
def start_search(params: SearchParams):
    result_box = []
    def thread_target():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(search_flight(params.dict()))
            result_box.append(result)
        except Exception as e:
            import traceback
            print("Errore nel thread di ricerca:", e)
            traceback.print_exc()
    t = threading.Thread(target=thread_target)
    t.start()
    t.join()
    return {"status": "OK", "results": result_box}

#@app.post('/search')
#def start_search(params: SearchParams, background_tasks: BackgroundTasks):
    # Fai funzionare come job in background
    #background_tasks.add_task(run_async_ricerca, params.dict())
    #return {"status": "Ricerca avviata!"}

def run_async_ricerca(params):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(search_flight(params))
    # Qui puoi anche salvare il risultato su disco o su DB
    pass