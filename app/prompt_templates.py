def build_prompt(city: str, days: int, traveler_type: str, places: list[dict], hotel: dict, restaurants: list[dict]) -> str:
    places_text = "\n".join(
        f"- **{p['name']}** — {p['description'] or 'No description'}"
        for p in places
    )

    restaurant_text = "\n".join(
        f"- **{r['name']}** — {r['description'] or 'No description'}"
        for r in restaurants
    )

    return f"""
You are a professional AI travel planner.

Create a personalized {days}-day itinerary for a trip to **{city}** tailored to a **{traveler_type}**.

🏨 **Hotel Recommendation**:
- **{hotel['name']}** – {hotel['description'] or 'No description'}

🧭 **Top Local Recommendations**:
These places are highly rated and relevant for this traveler. Integrate them naturally into the daily itinerary:

{places_text}

🍽️ **Recommended Restaurants**:
Use these real local restaurants in your daily lunch or dinner recommendations:

{restaurant_text}

📅 **Daily Plan**:
For each day:
- Morning and afternoon activities (include approximate time)
- Options for both good and bad weather
- One lunch and one dinner recommendation (use restaurants above when possible)

💡 Format the entire response using **markdown** with headers and bullet points.
🎯 Keep tone friendly, precise, and helpful.
🚫 Do not include breakfast unless explicitly requested.
"""
