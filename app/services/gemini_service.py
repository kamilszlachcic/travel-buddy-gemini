import vertexai
from vertexai.preview.generative_models import GenerativeModel
from app.prompt_templates import build_prompt
import markdown
vertexai.init(project="gold-summer-459311-q9", location="europe-west1")
model = GenerativeModel("gemini-2.0-flash-001")

from app.prompt_templates import build_prompt
from app.services.geoapify_service import get_coordinates, get_places
from app.services.scoring import score_place
from app.services.geoapify_service import get_hotels
from app.services.scoring import score_hotel
from app.services.geoapify_service import get_restaurants
from app.services.scoring import score_restaurant



async def generate_itinerary(city: str, days: int, traveler_type: str):
    from app.services.geoapify_service import get_hotels, get_restaurants
    from app.services.scoring import score_hotel, score_restaurant
    from app.prompt_templates import build_prompt

    # Pobierz współrzędne miasta
    lat, lon = await get_coordinates(city)

    # 1. Pobieranie i scoring hoteli
    raw_hotels = await get_hotels(lat, lon)
    hotels = [
        {
            "name": h["properties"]["name"],
            "description": h["properties"].get("formatted", ""),
            "score": score_hotel(h, traveler_type)
        }
        for h in raw_hotels.get("features", []) if h["properties"].get("name")
    ]
    top_hotels = sorted(hotels, key=lambda x: x["score"], reverse=True)[:1]

    # 2. Pobieranie i scoring restauracji
    raw_restaurants = await get_restaurants(lat, lon)
    restaurants = [
        {
            "name": r["properties"]["name"],
            "description": r["properties"].get("formatted", ""),
            "score": score_restaurant(r, traveler_type)
        }
        for r in raw_restaurants.get("features", []) if r["properties"].get("name")
    ]
    top_restaurants = sorted(restaurants, key=lambda x: x["score"], reverse=True)[:2]

    # 3. Pobieranie atrakcji (jeśli masz get_places jak wcześniej)
    raw_places = await get_places(lat, lon, categories="tourism", limit=15)
    places = [
        {
            "name": p["properties"]["name"],
            "description": p["properties"].get("formatted", ""),
            "score": score_place(p, traveler_type, is_bad_weather=False)
        }
        for p in raw_places.get("features", []) if p["properties"].get("name")
    ]
    top_places = sorted(places, key=lambda x: x["score"], reverse=True)[:3]

    # 4. Budowanie promptu
    prompt = build_prompt(city, days, traveler_type, top_places, top_hotels[0], top_restaurants)
    response = model.generate_content(prompt)

    return {
        "markdown": response.text,
        "html": markdown.markdown(response.text),
        "hotel": top_hotels[0],
        "restaurants": top_restaurants
    }

