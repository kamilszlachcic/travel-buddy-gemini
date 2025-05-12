from fastapi import FastAPI
from app.routers import trip
from app.routers import map_router

app = FastAPI(title="Travel Buddy Backend")

app.include_router(trip.router)
app.include_router(map_router.router)
