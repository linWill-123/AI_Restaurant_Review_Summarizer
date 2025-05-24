from fastapi import FastAPI, Query
from search_places import search_places
from fetch_reviews import fetch_reviews

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/places/")
def get_places(query: str = Query(...), location: str = None, radius: int = None):
    return search_places(query, location, radius)

@app.get("/reviews/{place_id}")
def get_reviews(place_id: str):
    return fetch_reviews(place_id)