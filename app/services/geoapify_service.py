import httpx
from app.utils.config import GEOAPIFY_API_KEY

BASE_URL = "https://api.geoapify.com/v2/places"

async def get_places(lat: float, lon: float, categories: str = "tourism", radius: int = 5000, limit: int = 10):
    params = {
        "categories": categories,
        "filter": f"circle:{lon},{lat},{radius}",  # UWAGA: lon, lat
        "bias": f"proximity:{lon},{lat}",
        "limit": limit,
        "apiKey": GEOAPIFY_API_KEY,
        "lang": "en"
    }

    print(f"[GEOAPIFY] Requesting places: {params}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
    except ReadTimeout:
        print("[GEOAPIFY] ❌ Request timed out.")
        return {"error": "Geoapify request timed out"}
    except httpx.HTTPStatusError as e:
        print(f"[GEOAPIFY] ❌ HTTP error: {e.response.status_code} - {e.response.text}")
        return {"error": f"Geoapify HTTP error {e.response.status_code}"}
    except Exception as e:
        print(f"[GEOAPIFY] ❌ Unexpected error: {e}")
        return {"error": "Unexpected error"}

async def get_coordinates(city: str) -> tuple[float, float]:
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": city,
        "apiKey": GEOAPIFY_API_KEY,
        "limit": 1,
        "lang": "en"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        coords = data["features"][0]["geometry"]["coordinates"]
        return coords[1], coords[0]  # lat, lon

async def get_hotels(lat: float, lon: float, radius: int = 5000, limit: int = 10):
    return await get_places(lat, lon, categories="accommodation.hotel", radius=radius, limit=limit)

async def get_restaurants(lat: float, lon: float, radius: int = 5000, limit: int = 10):
    return await get_places(lat, lon, categories="catering.restaurant", radius=radius, limit=limit)
