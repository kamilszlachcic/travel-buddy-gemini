# 🧭 Travel Buddy – AI-Powered Personalized Trip Companion

**Travel Buddy** is an intelligent assistant that generates **personalized travel itineraries** by combining LLM-driven conversational input with real-world data from multiple sources. The system integrates user profiles, contextual metadata, and POI scoring for high-quality, adaptable travel planning.

---

## 🚀 Project Goals

- Deliver tailored trip plans based on traveler type, preferences, group size, and context.
- Recommend points of interest (POIs) such as attractions, restaurants, and hotels using multi-source data.
- Visualize trip routes on interactive maps.
- Support multi-model LLM integration (Gemini, Claude, Mistral, etc.).
- Enable trip persistence, editing, and real-time refinement during the trip via chat interface.

---

## ✅ Key Features

### 🧠 Context-Aware Itinerary Generation
- Extracts structured `TripContext` from user input (city, days, persona, dietary needs, occasion, etc.).
- Uses this context to dynamically tailor each trip plan.

### 📍 POI Aggregation & Scoring
- **Yelp Dataset**:
  - Preprocessed locally (ETL via PySpark) including:
    - Review filtering and sentiment analysis
    - Feature extraction (tags, categories, ratings, etc.)
    - Deduplication and vectorization (FAISS indexing)
  - Used primarily for hotels and restaurants
- **Google Places API**:
  - Source for real-time attractions, backup hotel/restaurant data, coordinates
- **Tripadvisor API**:
  - Used to enrich POIs with semantic tags (`romantic`, `must-see`, etc.) and descriptions
- **Geoapify API**:
  - Coordinate enrichment and fallback POIs (e.g., niche regions)

### 🧠 LLM-Driven Plan Creation
- Uses Gemini via Vertex AI for generating detailed markdown itineraries.
- Supports dual-mode planning (e.g., good-weather vs bad-weather variants).

### 🗺️ Interactive Frontend
- **Streamlit** prototype:
  - Visual daily itineraries with POIs
  - Interactive map with coordinate pins
- **React** frontend (in progress):
  - Editable trips
  - Memory-enabled chatbot refinement

### 🔁 Persistent Planning
- Users can:
  - Save their trips
  - Reopen and edit past plans
  - Interact with the chatbot to improve their itinerary during the actual trip

---

## 🧩 Tech Stack

| Layer            | Technologies                                                                 |
|------------------|------------------------------------------------------------------------------|
| **Backend**      | Python, FastAPI, Vertex AI SDK, Geoapify, Google Places, Tripadvisor         |
| **Frontend**     | Streamlit (prototype), React (Tailwind, shadcn/ui)                           |
| **LLM Models**   | Gemini 2.0 Flash (via Vertex AI), with abstraction layer for Claude, Mistral |
| **Recommendation** | Custom scoring, PySpark, FAISS, POIBERT/BTRec (planned)                    |
| **Mapping**      | Geoapify (map + coordinates), Google Maps                                    |
| **Deployment**   | Docker-ready, GCP-compatible architecture                                    |

---

## 📂 Repository Structure

```
travel-buddy-gemini/
├── app/
│   ├── models/                    # Trip context and POI schemas
│   ├── routers/                   # FastAPI endpoints
│   ├── services/                 
│   │   ├── poi_engine.py         # Aggregation and scoring logic
│   │   ├── gemini_service.py     # LLM integration
│   │   └── external/             # API integrations (Yelp, Google, Geoapify)
│   ├── utils/                     # Prompt templates and helpers
├── data/                          # Preprocessed Yelp dataset
├── frontend/                      # Streamlit + React UI
├── examples/                      # Markdown sample trips
├── pyproject.toml, Dockerfile, .env, etc.
└── README.md
```

---

## 📊 Recommendation Engine (ML Plan)

### Hybrid POI Recommendation Approaches
- BERT-based sequence models for POI personalization (e.g. POIBERT, BTRec)
- Collaborative + content-based hybrid models to handle cold start
- Sentiment-aware ranking using NLP over reviews (spaCy, Hugging Face)

### FAISS Integration
- Vectorized POIs allow for fast similarity search and persona matching
- Personalized re-ranking using distance to traveler vector

---

## 📈 Future Roadmap

### Phase 1 (Completed)
- ✅ Gemini integration and prompt design
- ✅ Context extraction and trip logic
- ✅ Yelp dataset ETL, tagging, scoring, FAISS vector search

### Phase 2 (WIP)
- ⏳ POI fusion from Google, Tripadvisor, Yelp
- ⏳ React frontend with editable UI
- ⏳ A/B testing and feedback loop for plan quality

### Phase 3 (Planned)
- 🔄 Real-time trip editing via chatbot
- 📅 Event-based recommendations (festivals, seasonal offers)
- 🧠 Dynamic model retraining (Airflow, MLflow)
- 📊 Real-time analytics (Prometheus, Grafana)

---

## 🤖 Example Output (Markdown)

```markdown
### Day 1 – Food Lover's Tour of Barcelona

**Morning**: Gothic Quarter walk + local pastry  
**Lunch**: Tapas at El Xampanyet  
**Afternoon**: Picasso Museum + Chocolate tasting  
**Dinner**: Seafood paella at Bodega Biarritz  
**Evening**: Jazz bar in El Raval  

[Interactive map here]
```

---

## 🙋 Author

- **Kamil Szlachcic**  
  GitHub: [@kamilszlachcic](https://github.com/kamilszlachcic)  
  LinkedIn: [Kamil Szlachcic](https://www.linkedin.com/in/kamilszlachcic)

---

## 📃 License

MIT License – see `LICENSE` for details.