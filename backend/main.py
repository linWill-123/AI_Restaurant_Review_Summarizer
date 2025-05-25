from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from search_places import search_places
from fetch_reviews import fetch_reviews

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/places/")
def get_places(query: str = Query(...), location: str = None, radius: int = None):
    return search_places(query, location, radius)

@app.get("/reviews/{place_id}")
def get_reviews(place_id: str):
    return fetch_reviews(place_id)