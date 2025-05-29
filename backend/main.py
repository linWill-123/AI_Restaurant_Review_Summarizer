from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from search_places import search_places
from fetch_reviews import fetch_reviews
from embeddings import embed_texts
from faiss_index import FaissIndex
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

faiss_idx = FaissIndex(dim=384, use_gpu=False)

class IndexRequest(BaseModel):
     place_id: str
     snippets: list[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/places/")
def get_places(query: str = Query(...), location: str = None, radius: int = None):
    return search_places(query, location, radius)

@app.get("/reviews/{place_id}")
def get_reviews(place_id: str):
    return fetch_reviews(place_id)

@app.post("/index_reviews/")
def index_reviews(req: IndexRequest):
    # Convert texts to embeddings
    embs = embed_texts(req.snippets)
    # Add embeddings to the index
    faiss_idx.add_embeddings(embs)
    return {"indexed_count": len(embs)}