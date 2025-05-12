# 🧭 Travel Buddy – AI-Powered Personalized Trip Planner

**Travel Buddy** is an intelligent travel assistant powered by Large Language Models (LLMs), designed to generate **personalized travel itineraries** based on user preferences, context, and local data. The project focuses on modularity, open-source integration, and a modern NLP/GenAI backend.

---

## 🚀 Project Goals

- Deliver customized travel plans for different traveler types and occasions.
- Recommend attractions, hotels, restaurants, and nightlife options.
- Provide interactive maps and routing with POI (Point of Interest) coordinates.
- Leverage open data sources and generative models to enhance UX.
- Offer an adaptable architecture that supports different models and frontends.

---

## ✅ Current Progress

### 🧠 Backend
- Fully functional **FastAPI** server with modular endpoints for itinerary generation, POI enrichment, and user queries.
- Integrated with **Google Vertex AI** using `gemini-2.0-flash-001`.
- Implemented prompt-engineering logic for itinerary generation using user-defined templates.
- Defined user personas via `traveler_types.py` for contextual itinerary suggestions.
- Created modular structure for:
  - Generating itineraries based on location, number of days, and occasion.
  - Generating coordinates for POIs (Geoapify / Gemini fallback).
- Added support for restaurant and hotel recommendations with multiple entries per day.
- Established flexible design for activity slotting (morning, afternoon, evening).
- Implemented markdown formatting to support consistent frontend rendering.

### 🌐 Frontend
- Functional **Streamlit** prototype for displaying itineraries and interacting with the backend.
- Designed interactive map component (WIP).
- Structured visual itinerary display per day.
- Supports future click-to-expand POI details (e.g., external links, tags).

---

## 📍 Features (Planned & In Progress)

| Feature | Description | Status |
|--------|-------------|--------|
| **Dynamic Recommendation Engine** | Score attractions/restaurants based on distance, popularity, activity type, weather (fallback logic), etc. | ⏳ In planning |
| **Dual-mode activity planning** | If weather is relevant (e.g., hiking, beach), offer both sunny and rainy-day variants | ✅ Ready |
| **Map route visualization** | Plot full trip path across POIs and allow filtering | ⏳ In design |
| **Geoapify / OpenTripMap Integration** | For obtaining coordinates, metadata, and type-based filtering | ⏳ Prototype |
| **RAG architecture (LLM + local context)** | Integrate semantic search (e.g., FAISS + LangChain) for personalized local knowledge recommendations | ⏳ Research |
| **Traveler memory** | Retain short-term context during multi-turn interactions | ✅ LLM memory integration |
| **Model fallback / switching** | Abstract model interface to toggle between Gemini, Claude, Mistral, etc. | ⏳ Planning |

---

## 🧩 Tech Stack

- **Backend**: FastAPI, Python, Vertex AI SDK, Geoapify API
- **Frontend**: Streamlit (prototype), React (Tailwind, WIP), shadcn/ui
- **LLM Integration**: Google Gemini 2.0 Flash
- **Mapping & Coordinates**: Geoapify (fallback to Gemini)
- **Prompt Templates**: Custom YAML-style prompt abstraction
- **Deployment**: Docker-ready, GCP-compatible

---

## 🗂️ Repository Structure

```
travel-buddy-gemini/
│
├── app/
│   ├── models/
│   │   └── traveler_types.py           # User profiles/personas
│   │
│   ├── routers/
│   │   ├── map_router.py               # Routing endpoints
│   │   └── trip.py                     # Trip planning endpoint
│   │
│   ├── services/
│   │   ├── gemini_service.py           # LLM integration (Vertex AI)
│   │   ├── geoapify_service.py         # POI coordinate enrichment
│   │   ├── map_services.py             # Geo/map logic
│   │   └── scoring.py                  # Scoring engine for recommendations
│   │
│   ├── utils/
│   │   ├── main.py                     # FastAPI app definition
│   │   └── prompt_templates.py         # Prompt logic and templating
│
├── examples/
│   └── sample_output.md                # Markdown-based itinerary sample
│
├── streamlit_app.py                    # Streamlit UI prototype
├── .env                                # Environment variables
├── .gitignore
├── poetry.lock
├── pyproject.toml
└── README.md
│
├── app/
│   ├── main.py                  # FastAPI backend entry point
│   ├── prompt_templates.py      # Prompt logic and templating
│   ├── traveler_types.py        # User profiles/personas
│   ├── geoapify_service.py      # Location data integration
│   └── itinerary_generator.py   # Core trip logic
│
├── frontend/
│   └── streamlit_app.py         # Streamlit UI prototype
│
├── tests/                       # Unit and integration tests (TBD)
│
└── README.md                    # You're here
```

---

## 🛣 Roadmap

1. **LLM Tuning & Evaluation**
   - Add scoring logic (popularity, proximity, etc.)
   - Use structured output schema for map parsing

2. **Frontend Completion**
   - Interactive, mobile-first view with filters
   - Dynamic rendering of daily schedules and links

3. **Data Enhancements**
   - Expand POI metadata with crowd-sourced or open government APIs
   - Introduce event-based filtering (e.g., festivals, seasonal attractions)

4. **AI Reasoning Layer**
   - Contextual filtering (e.g., museums in bad weather, trails in good)
   - Fallback logic for ambiguous queries (ask clarifying questions)

---

## 🤖 Example Output

A 3-day trip to Barcelona for a food lover might return:

```markdown
### Day 1 – Exploring Gothic Quarter

**Morning**: Walk through Barri Gòtic, visit Barcelona Cathedral  
**Lunch**: Local tapas at El Xampanyet  
**Afternoon**: Picasso Museum + Chocolate tasting  
**Dinner**: Bodega Biarritz 1881  
**Nightlife**: Jazz club near Plaça Reial  

[Map with pins and routes to be displayed here]
```

---

## 📌 License

MIT License – see `LICENSE` for details.

---

## 🙋‍♂️ Authors

- **Kamil Szlachcic** – [GitHub](https://github.com/kamilszlachcic) | [LinkedIn](https://www.linkedin.com/in/kamilszlachcic)

---

## 🌟 Contribute

We’re open to ideas, contributions, and feedback on how to make Travel Buddy even smarter and more useful. PRs and discussions welcome.