from typing import List
from app.services.context_extraction import TripContext

# Mock POI type – to be later replaced with structured POI dataclass or Pydantic model
class POI(dict):
    pass

def generate_poi_recommendations(trip_context: TripContext) -> List[POI]:
    """
    Generates a list of recommended POIs from multiple sources
    based on the structured TripContext.
    """
    # TODO: Integrate Yelp, Google Places, OpenTripMap etc.

    # Mock example data – to be replaced with real engine logic
    mock_pois = [
        POI({
            "name": "Modern Art Museum",
            "source": "OpenTripMap",
            "category": "Museum",
            "rating": 4.6,
            "tags": ["cultural", "indoor"],
            "description": "Contemporary exhibitions with free audio tours.",
            "coordinates": [40.7128, -74.0060]
        }),
        POI({
            "name": "Trattoria da Luigi",
            "source": "Yelp",
            "category": "Restaurant",
            "rating": 4.8,
            "tags": ["vegetarian-friendly", "romantic"],
            "description": "Cozy Italian place with vegan options.",
            "coordinates": [40.7130, -74.0055]
        })
    ]

    return mock_pois
