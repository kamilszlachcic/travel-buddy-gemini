from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.models.traveler_types import TravelerType
from app.services.gemini_service import generate_itinerary
from app.services.geoapify_service import get_coordinates, get_places, get_hotels, get_restaurants
from app.services.scoring import score_place
from vertexai.preview.generative_models import GenerativeModel

router = APIRouter(prefix="/chat", tags=["Trip Planner"])

def map_traveler_type(model_type: str) -> str:
    mapping = {
        "luxury": "romantic spirit",
        "budget": "backpacker",
        "authentic": "authentic explorer",
        "comfortable": "comfort traveler",
        "nature": "outdoor enthusiast",
        "slow": "slow traveler",
        "influencer": "influencer trail explorer"
    }
    return mapping.get(model_type.lower(), model_type)



# ---------- Classic Trip Planning Endpoint ----------

class TripRequest(BaseModel):
    city: str
    days: int
    traveler_type: TravelerType


@router.post("/trip-plan")
async def trip_plan(req: TripRequest):
    result = await generate_itinerary(
        req.city,
        req.days,
        req.traveler_type.value
    )
    return result


# ---------- Location Info + Scoring ----------

@router.get("/local-info")
async def local_info(city: str = "Lisbon", category: str = "tourism.sights", traveler_type: TravelerType = TravelerType.comfort_traveler, bad_weather: bool = False):
    lat, lon = await get_coordinates(city)
    places = await get_places(lat, lon, categories=category)

    scored = [
        {
            "name": p["properties"]["name"],
            "score": score_place(p, traveler_type.value, bad_weather),
            "raw": p
        }
        for p in places.get("features", []) if p["properties"].get("name")
    ]
    scored = sorted(scored, key=lambda x: x["score"], reverse=True)

    return scored[:5]


@router.get("/hotels")
async def hotels(city: str = "Lisbon"):
    lat, lon = await get_coordinates(city)
    hotels = await get_hotels(lat, lon)
    return hotels


# ---------- Conversational Mode ----------

class Message(BaseModel):
    role: str  # "user" or "model"
    content: str


class ConversationRequest(BaseModel):
    messages: List[Message]


@router.post("/conversation")
async def conversation(req: ConversationRequest):
    import json

    model = GenerativeModel("gemini-2.0-flash-001")
    chat = model.start_chat()

    system_instruction = """
You are a travel assistant. Based on the user's message, summarize key travel info:
- Destination
- Number of days
- Occasion (e.g. honeymoon, family trip)
- Traveler type (e.g. romantic spirit, comfort traveler)

Respond in valid JSON format.
"""

    user_combined = "\n".join([m.content for m in req.messages])
    full_prompt = f"{system_instruction}\n\nConversation:\n{user_combined}"

    response = chat.send_message(full_prompt)

    try:
        clean_text = re.sub(r"```json|```", "", response.text).strip()
        parsed = json.loads(clean_text)
        traveler_type_mapped = map_traveler_type(parsed["traveler_type"])

        plan = await generate_itinerary(
            city=parsed["destination"],
            days=parsed["number_of_days"],
            traveler_type=traveler_type_mapped
        )

        return {
            "metadata": parsed,
            "itinerary": plan
        }

    except Exception as e:
        return {"error": str(e), "raw": response.text}