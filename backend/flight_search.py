from typing import Optional
from playwright.async_api import async_playwright
import random
import asyncio
from datetime import datetime, timedelta

async def random_delay(min_ms=1000, max_ms=3000):
    delay = random.randint(min_ms, max_ms) / 1000
    await asyncio.sleep(delay)

def is_weekend(date):
    """Verifica se una data cade nel weekend (sabato=5 o domenica=6)"""
    return date.weekday() >= 5

def check_weekend_requirements(current_date, return_date, weekend_requirement='none'):
    """
    Parameters:
    weekend_requirement (str): 
        'none' - nessun requisito weekend
        'one' - almeno un giorno del weekend
        'both' - entrambi i giorni del weekend
        'full' - tutto il weekend (sabato e domenica)
    """
    if weekend_requirement == 'none':
        return True
        
    # Crea lista di tutte le date del viaggio
    dates = []
    while current_date <= return_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    weekend_days = sum(1 for d in dates if is_weekend(d))
    
    if weekend_requirement == 'one':
        return weekend_days >= 1
    elif weekend_requirement == 'both':
        return weekend_days >= 2
    elif weekend_requirement == 'full':
        # Verifica se c'è sia sabato che domenica
        has_saturday = any(d.weekday() == 5 for d in dates)
        has_sunday = any(d.weekday() == 6 for d in dates)
        return has_saturday and has_sunday
    
    return False

async def create_search_url(departure_airport, arrival_airport, departure_date, return_date):
    url = f"https://www.kiwi.com/en/search/results/{departure_airport}-italy/{arrival_airport}-turkey/{departure_date}/{return_date}?times=0-11-0-24_15-24-0-24&stopNumber=0%7Etrue"
    return url

def find_flight_by_id(itineraries, flight_id):
    for itinerary in itineraries:
        if itinerary['id'] == flight_id:
            return itinerary
    return None

def format_flight_data(flight):
    outbound = flight['outbound']['sectorSegments'][0]['segment']
    outbound_departure_time = outbound['source']['localTime']
    outbound_arrival_time = outbound['destination']['localTime']
    outbound_duration = outbound['duration']
    outbound_carrier = outbound['carrier']['name']

    inbound = flight['inbound']['sectorSegments'][0]['segment']
    inbound_departure_time = inbound['source']['localTime']
    inbound_arrival_time = inbound['destination']['localTime']
    inbound_duration = inbound['duration']
    inbound_carrier = inbound['carrier']['name']

    price = float(flight['price']['amount'])
    
    flight_info = {
        "andata": {
            "orario partenza": outbound_departure_time,
            "orario arrivo": outbound_arrival_time,
            "durata volo": outbound_duration // 60,
            "compagnia aerea": outbound_carrier
        },
        "ritorno": {
            "orario partenza": inbound_departure_time,
            "orario arrivo": inbound_arrival_time,
            "durata volo": inbound_duration // 60,
            "compagnia aerea": inbound_carrier
        },
        "prezzo": price
    }

    return flight_info

async def handle_response(response, departure_date, return_date, results_list):
    if "https://api.skypicker.com/umbrella/v2/graphql?featureName=SearchReturnItinerariesQuery" in response.url:
        try:
            # Verifica che la risposta sia OK
            if not response.ok:
                print(f"Risposta non valida: {response.status}")
                return

            # Prova a ottenere il contenuto della risposta
            try:
                data = await response.json()
            except Exception as e:
                print(f"Errore nel parsing JSON: {e}")
                text = await response.text()
                print(f"Contenuto della risposta: {text[:200]}...")  # Stampa i primi 200 caratteri
                return

            # Verifica che i dati contengano le chiavi necessarie
            if not data.get('data', {}).get('returnItineraries', {}).get('itineraries'):
                print("Struttura JSON non valida o dati mancanti")
                return

            itineraries = data['data']['returnItineraries']['itineraries']
            topResults = data['data']['returnItineraries']['metadata']['topResults']

            if not itineraries or not topResults:
                print("Nessun volo trovato")
                return

            best_flight_id = topResults.get('best', {}).get('id')
            cheapest_flight_id = topResults.get('cheapest', {}).get('id')

            if not best_flight_id or not cheapest_flight_id:
                print("ID dei voli mancanti")
                return

            best_flight = find_flight_by_id(itineraries, best_flight_id)
            cheapest_flight = find_flight_by_id(itineraries, cheapest_flight_id)

            if not best_flight or not cheapest_flight:
                print("Impossibile trovare i voli con gli ID specificati")
                return

            formatted_data = {
                "search_date": {
                    "departure": departure_date,
                    "return": return_date
                },
                "best_flight": format_flight_data(best_flight),
                "cheapest_flight": format_flight_data(cheapest_flight)
            }

            results_list.append(formatted_data)
            print(f"Aggiunto risultato per la ricerca {departure_date}->{return_date}")
            return

        except Exception as e:
            print(f"Errore generale nel processare la risposta: {e}")

async def search_flight(params: dict):
    departure_airport = params['departure_airport']
    arrival_airport = params['arrival_airport']
    departure_month = params['departure_month']
    start_day = params['start_day']
    trip_duration = params['trip_duration']
    weekend_requirement = params['weekend_requirement'] # 'none', 'one', 'both', 'full'
    results_list = []

    year, month = map(int, departure_month.split('-'))
    
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = (next_month - timedelta(days=1)).day

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        for day in range(start_day, last_day + 1):
            departure_date = datetime(year, month, day)
            return_date = departure_date + timedelta(days=trip_duration)

            if not check_weekend_requirements(departure_date, return_date, weekend_requirement):
                print(f"Skip date {departure_date.strftime('%Y-%m-%d')} - non soddisfa i requisiti del weekend")
                continue
            
            departure_str = departure_date.strftime("%Y-%m-%d")
            return_str = return_date.strftime("%Y-%m-%d")
            
            page = await context.new_page()
            # Variabile per tracciare se abbiamo già salvato i dati per questa ricerca
            response_processed = False

            async def handle_response_wrapper(response):
                nonlocal response_processed
                if not response_processed and "https://api.skypicker.com/umbrella/v2/graphql?featureName=SearchReturnItinerariesQuery" in response.url:
                    await handle_response(response, departure_str, return_str, results_list)
                    response_processed = True

            # Aggiungi il listener
            page.on("response", handle_response_wrapper)
            
            url = await create_search_url(
                departure_airport=departure_airport,
                arrival_airport=arrival_airport,
                departure_date=departure_str,
                return_date=return_str
            )
            
            print(f"Cercando voli: Partenza: {departure_str}, Ritorno: {return_str}")
            
            try:
                await page.goto(url)
                #await page.wait_for_load_state("networkidle")
                await random_delay(2000, 5000)
                
            except Exception as e:
                print(f"Errore durante la ricerca per il giorno {departure_str}: {e}")
                continue
            finally:
                await page.close()
        
        await browser.close()
        results_list.sort(key=lambda x: x["cheapest_flight"]["prezzo"])
        return results_list