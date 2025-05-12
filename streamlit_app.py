import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

API_URL = "http://localhost:8000/chat/map-data"

st.set_page_config(page_title="Travel Buddy Map", layout="wide")
st.title("🗺️ Travel Buddy – Map View")

# --- User input ---
col1, col2 = st.columns(2)
with col1:
    destination = st.text_input("Destination", value="Lisbon")
with col2:
    traveler_type = st.selectbox("Traveler Type", [
        "romantic spirit", "comfort traveler", "backpacker", "authentic explorer", "outdoor enthusiast", "slow traveler", "influencer trail explorer"
    ])

# --- Fetch data ---
params = {
    "destination": destination,
    "traveler_type": traveler_type,
    "format": "json"
}

resp = requests.get(API_URL, params=params)

if resp.status_code != 200:
    st.error(f"Error fetching data: {resp.status_code}")
else:
    pois = resp.json()

    if not pois:
        st.warning("No results found.")
    else:
        # --- Show table ---
        st.subheader("📋 Ranked Places")
        st.dataframe([
            {
                "Name": p["name"],
                "Type": p["type"],
                "Category": p["category"],
                "Score": p["score"]
            } for p in pois
        ])

        # --- Show map ---
        st.subheader("🗺️ Map View")
        center = [pois[0]["lat"], pois[0]["lon"]]
        fmap = folium.Map(location=center, zoom_start=13)

        for p in pois:
            popup = f"{p['name']} ({p['type']})<br>Score: {p['score']}"
            color = {
                "hotel": "blue",
                "restaurant": "green",
                "sight": "red"
            }.get(p["type"], "gray")

            folium.Marker(
                location=[p["lat"], p["lon"]],
                popup=popup,
                icon=folium.Icon(color=color)
            ).add_to(fmap)

        st_data = st_folium(fmap, width=900, height=600)
