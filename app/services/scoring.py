def score_place(place: dict, traveler_type: str, is_bad_weather: bool) -> float:
    score = 0

    category = place.get("properties", {}).get("categories", [])
    name = place.get("properties", {}).get("name", "").lower()

    # 1. Weather_preference
    if is_bad_weather and any(cat in category for cat in ["entertainment.museum", "catering.cafe"]):
        score += 3
    elif not is_bad_weather and any(cat in category for cat in ["tourism.sights", "natural.park"]):
        score += 3

    # 2. Traveler_type
    if traveler_type == "authentic explorer" and "historic" in name:
        score += 2
    if traveler_type == "romantic spirit" and any(kw in name for kw in ["view", "garden", "romantic"]):
        score += 2
    if traveler_type == "backpacker" and "cheap" in name:
        score += 1

    # 3. Scoring
    if "rate" in place.get("properties", {}):
        score += float(place["properties"]["rate"])

    return score


def score_hotel(hotel: dict, traveler_type: str) -> float:
    score = 0
    name = hotel.get("properties", {}).get("name", "").lower()
    category = hotel.get("properties", {}).get("categories", [])

    # Przykładowe heurystyki
    if traveler_type == "romantic spirit" and "spa" in name:
        score += 3
    if traveler_type == "backpacker" and "hostel" in name:
        score += 3
    if traveler_type == "comfort traveler" and "resort" in name:
        score += 2
    if "luxury" in name or "boutique" in name:
        score += 2

    # Ocena wg Geoapify (jeśli dostępna)
    if "rate" in hotel["properties"]:
        score += float(hotel["properties"]["rate"])

    return score


def score_restaurant(place: dict, traveler_type: str) -> float:
    score = 0
    name = place.get("properties", {}).get("name", "").lower()

    if traveler_type == "romantic spirit" and any(k in name for k in ["wine", "romantic", "bistro"]):
        score += 3
    if traveler_type == "authentic explorer" and any(k in name for k in ["local", "tavern", "kitchen"]):
        score += 2
    if traveler_type == "comfort traveler" and "brasserie" in name:
        score += 2
    if traveler_type == "backpacker" and "bar" in name:
        score += 1

    if "rate" in place["properties"]:
        score += float(place["properties"]["rate"])

    return score
