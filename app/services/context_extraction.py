from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.gemini_service import call_gemini_json

class TripContext(BaseModel):
    city: str
    days: int
    persona: Optional[str] = None
    preferred_categories: List[str] = Field(default_factory=list)
    group_type: List[str] = Field(default_factory=list)
    budget_level: Optional[str] = None  # e.g., "Low", "Mid-range", "High"
    dietary_preferences: List[str] = Field(default_factory=list)
    mobility: Optional[str] = None      # e.g., "Walking", "Driving"
    season: Optional[str] = None        # e.g., "Winter", "Summer"
    occasion: Optional[str] = None      # e.g., "Honeymoon", "Business"

def extract_trip_context_from_prompt(user_message: str) -> TripContext:
    """
    Sends user message to Gemini and expects a JSON with structured travel context.
    """
    prompt = f"""
    Extract structured travel context from the following user message. 
    Return only valid JSON with the following fields:
    city (str), days (int), persona (str), preferred_categories (List[str]), 
    group_type (List[str]), budget_level (str), dietary_preferences (List[str]),
    mobility (str), season (str), occasion (str)

    Message: "{user_message}"
    """
    try:
        response_json = call_gemini_json(prompt)
        return TripContext(**response_json)
    except Exception as e:
        print(f"⚠️ Failed to extract context: {e}")
        raise ValueError("Failed to extract TripContext from message")
