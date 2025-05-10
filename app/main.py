from fastapi import FastAPI
from app.routers import trip

app = FastAPI(title="Travel Buddy Backend")

app.include_router(trip.router)