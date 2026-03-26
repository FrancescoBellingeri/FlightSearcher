from rebrowser_playwright.async_api import async_playwright, Browser
import random
import asyncio
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

async def random_delay(min_ms=1000, max_ms=3000):
    delay = random.randint(min_ms, max_ms) / 1000
    await asyncio.sleep(delay)

def is_weekend(date):
    """Returns True if the date falls on a weekend (Saturday=5 or Sunday=6)."""
    return date.weekday() >= 5

def check_weekend_requirements(current_date, return_date, weekend_requirement='none'):
    """
    Parameters:
    weekend_requirement (str):
        'none' - no weekend requirement
        'one'  - at least one weekend day
        'full' - full weekend (both Saturday and Sunday)
    """
    if weekend_requirement == 'none':
        return True

    dates = []
    while current_date <= return_date:
        dates.append(current_date)
        current_date += timedelta(days=1)

    weekend_days = sum(1 for d in dates if is_weekend(d))

    if weekend_requirement == 'one':
        return weekend_days >= 1
    elif weekend_requirement == 'full':
        has_saturday = any(d.weekday() == 5 for d in dates)
        has_sunday = any(d.weekday() == 6 for d in dates)
        return has_saturday and has_sunday

    return False

async def create_search_url(departure_airport, arrival_airport, departure_date, return_date, times=None, stop_number=None):
    url = f"https://www.kiwi.com/en/search/results/{departure_airport}/{arrival_airport}/{departure_date}/{return_date}"
    params = []
    if times:
        params.append(f"times={times}")
    if stop_number is not None:
        params.append(f"stopNumber={stop_number}%7Etrue")
    if params:
        url += "?" + "&".join(params)
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
    outbound_departure_airport = outbound['source']['station']['name']
    outbound_arrival_airport = outbound['destination']['station']['name']

    inbound = flight['inbound']['sectorSegments'][0]['segment']
    inbound_departure_time = inbound['source']['localTime']
    inbound_arrival_time = inbound['destination']['localTime']
    inbound_duration = inbound['duration']
    inbound_carrier = inbound['carrier']['name']
    inbound_departure_airport = inbound['source']['station']['name']
    inbound_arrival_airport = inbound['destination']['station']['name']

    price = float(flight['price']['amount'])

    return {
        "outbound": {
            "departure_time": outbound_departure_time,
            "arrival_time": outbound_arrival_time,
            "duration": outbound_duration // 60,
            "carrier": outbound_carrier,
            "departure_airport": outbound_departure_airport,
            "arrival_airport": outbound_arrival_airport,
        },
        "inbound": {
            "departure_time": inbound_departure_time,
            "arrival_time": inbound_arrival_time,
            "duration": inbound_duration // 60,
            "carrier": inbound_carrier,
            "departure_airport": inbound_departure_airport,
            "arrival_airport": inbound_arrival_airport,
        },
        "price": price,
    }

async def handle_response(response, departure_date, return_date, results_list, search_url=None):
    if "https://api.skypicker.com/umbrella/v2/graphql?featureName=SearchReturnItinerariesQuery" in response.url:
        try:
            if not response.ok:
                logger.warning(f"Invalid response: {response.status}")
                return

            try:
                data = await response.json()
            except Exception as e:
                logger.error(f"JSON parsing error: {e}")
                text = await response.text()
                logger.error(f"Response content: {text[:200]}...")
                return

            if not data.get('data', {}).get('returnItineraries', {}).get('itineraries'):
                logger.warning("Invalid JSON structure or missing data")
                return

            itineraries = data['data']['returnItineraries']['itineraries']
            top_results = data['data']['returnItineraries']['metadata']['topResults']

            if not itineraries or not top_results:
                logger.info("No flights found")
                return

            best_flight_id = top_results.get('best', {}).get('id')
            cheapest_flight_id = top_results.get('cheapest', {}).get('id')

            if not best_flight_id or not cheapest_flight_id:
                logger.warning("Missing flight IDs")
                return

            best_flight = find_flight_by_id(itineraries, best_flight_id)
            cheapest_flight = find_flight_by_id(itineraries, cheapest_flight_id)

            if not best_flight or not cheapest_flight:
                logger.warning("Could not find flights with the specified IDs")
                return

            formatted_data = {
                "search_date": {
                    "departure": departure_date,
                    "return": return_date,
                },
                "best_flight": format_flight_data(best_flight),
                "cheapest_flight": format_flight_data(cheapest_flight),
                "search_url": search_url,
            }

            results_list.append(formatted_data)
            logger.info(f"Result added for search {departure_date}->{return_date}")

        except Exception as e:
            logger.error(f"General error processing response: {e}")

async def search_flight(params: dict, browser: Browser):
    departure_airport = params['departure_airport']
    arrival_airport = params['arrival_airport']
    departure_month = params['departure_month']
    start_day = params['start_day']
    trip_duration = params['trip_duration']
    weekend_requirement = params['weekend_requirement']
    times = params.get('times')
    stop_number = params.get('stop_number')

    year, month = map(int, departure_month.split('-'))

    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = (next_month - timedelta(days=1)).day

    total_days = last_day - start_day + 1
    yield {"type": "init", "total": total_days}

    results_list = []
    completed = 0

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]

    context = await browser.new_context(
        user_agent=random.choice(user_agents),
        viewport={"width": 1920, "height": 1080}
    )

    try:
        for day in range(start_day, last_day + 1):
            departure_date = datetime(year, month, day)
            return_date = departure_date + timedelta(days=trip_duration)
            departure_str = departure_date.strftime("%Y-%m-%d")
            return_str = return_date.strftime("%Y-%m-%d")

            if not check_weekend_requirements(departure_date, return_date, weekend_requirement):
                completed += 1
                yield {"type": "skip", "date": departure_str, "completed": completed}
                continue

            yield {"type": "progress", "completed": completed, "current_date": departure_str}

            prev_count = len(results_list)

            url = await create_search_url(
                departure_airport=departure_airport,
                arrival_airport=arrival_airport,
                departure_date=departure_str,
                return_date=return_str,
                times=times,
                stop_number=stop_number,
            )

            page = await context.new_page()
            response_processed = False

            async def handle_response_wrapper(response, _dep=departure_str, _ret=return_str, _url=url):
                nonlocal response_processed
                if not response_processed and "https://api.skypicker.com/umbrella/v2/graphql?featureName=SearchReturnItinerariesQuery" in response.url:
                    await handle_response(response, _dep, _ret, results_list, _url)
                    response_processed = True

            page.on("response", handle_response_wrapper)

            logger.info(f"Searching flights: Departure: {departure_str}, Return: {return_str}")

            try:
                await page.goto(url)
                timeout_seconds = 15
                for _ in range(timeout_seconds * 2):
                    if response_processed:
                        break
                    await asyncio.sleep(0.5)

                if not response_processed:
                    logger.warning(f"Timeout for search {departure_str}->{return_str}")

                await random_delay(2000, 5000)

            except Exception as e:
                logger.error(f"Error searching for day {departure_str}: {e}")
            finally:
                await page.close()

            completed += 1
            if len(results_list) > prev_count:
                yield {"type": "result", "data": results_list[-1], "completed": completed}
            else:
                yield {"type": "progress", "completed": completed, "current_date": None}

    finally:
        await context.close()

    yield {"type": "done", "total_found": len(results_list)}
