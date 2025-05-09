def build_prompt(city, days, traveler_type):
    return f"""
You are a travel planner.

Create a detailed {days}-day travel itinerary to {city} for a traveler who is a {traveler_type}.

Include the following:
1. General plan per day with recommended activities and timing.
2. At the beginning, suggest **one** hotel (3★ or higher if applicable), including name and short description.
3. For **each day**, include:
   - One lunch recommendation (local, casual or authentic)
   - One dinner recommendation (more special or atmospheric)

Do not include breakfast unless specifically requested.

Keep the tone friendly but professional. Return the response in **markdown** format.
"""
