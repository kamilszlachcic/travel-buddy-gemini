from vertexai.preview.generative_models import GenerativeModel
from app.prompt_templates import build_prompt

model = GenerativeModel("gemini-1.5-pro")

def generate_itinerary(city: str, days: int, traveler_type: str) -> str:
    prompt = build_prompt(city, days, traveler_type)
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    plan = generate_itinerary("Lisbon", 4, "authentic explorer")
    print(plan)
