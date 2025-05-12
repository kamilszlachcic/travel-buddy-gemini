from fastapi import APIRouter
from app.services.map_services import fetch_and_format_poi, to_geojson

router = APIRouter(prefix="/chat", tags=["Map & Location"])


@router.get("/map-data")
async def get_map_data(destination: str, traveler_type: str = "default", format: str = "json"):
    poi_list = await fetch_and_format_poi(destination, traveler_type)

    if format == "geojson":
        return to_geojson(poi_list)

    return poi_list
