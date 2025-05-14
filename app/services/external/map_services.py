from app.services.external.geoapify_service import get_coordinates, get_places
from app.services.scoring import score_place, score_hotel, score_restaurant

async def fetch_and_format_poi(destination: str, traveler_type: str = "default"):
    lat, lon = await get_coordinates(destination)

    places = await get_places(lat, lon, categories="tourism.sights")
    hotels = await get_places(lat, lon, categories="accommodation.hotel")
    restaurants = await get_places(lat, lon, categories="catering.restaurant")

    def extract_poi(poi, poi_type):
        props = poi.get("properties", {})
        name = props.get("name")
        lat_, lon_ = props.get("lat"), props.get("lon")

        if not (name and lat_ and lon_):
            return None

        try:
            score_func = {
                "sight": score_place,
                "hotel": score_hotel,
                "restaurant": score_restaurant
            }.get(poi_type, lambda x, y: 0.0)

            score = score_func(poi, traveler_type)

        except Exception as e:
            print(f"[SCORING ERROR] {e} — {name}")
            score = 0.0

        return {
            "name": name,
            "type": poi_type,
            "lat": lat_,
            "lon": lon_,
            "category": props.get("subclass", "unknown"),
            "score": round(score, 3)
        }

    def filter_valid(pois, poi_type):
        return list(filter(None, (extract_poi(p, poi_type) for p in pois.get("features", []))))

    return (
        filter_valid(places, "sight") +
        filter_valid(hotels, "hotel") +
        filter_valid(restaurants, "restaurant")
    )


def to_geojson(poi_list: list[dict]):
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": p["name"],
                    "type": p["type"],
                    "category": p["category"],
                    "score": p["score"]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [p["lon"], p["lat"]]
                }
            }
            for p in poi_list
        ]
    }
