from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from search_places import search_places
from fetch_reviews import fetch_reviews
from retrieve_snippets import retrieve_snippets
from embeddings import embed_texts
from pydantic import BaseModel
from prompts import user_template

from shared import faiss_idx, all_snippets
from llm_chain import summarization_chain


app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class SummarizeRequest(BaseModel):
    attribute: str 
    k: int = 3 

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
    # First reset the FAISS index and clear out any existing snippets
    global faiss_idx, all_snippets
    faiss_idx.reset()
    all_snippets.clear()

    # Convert texts to embeddings
    embs = embed_texts(req.snippets)
    # Add embeddings to the index
    faiss_idx.add_embeddings(embs)
    # store raw snippets for later retrieval mapping
    all_snippets.extend(req.snippets)
    return {"indexed_count": len(embs)}

@app.post("/summarize/")
async def summarize(req: SummarizeRequest):
    """
    1) Retrieve top-k review snippets for the requested attribute.
    2) Build the prompt context (list each snippet with a leading dash).
    3) Invoke the LLM chain to produce a three-sentence summary.
    """
    # a) Retrieve relevant snippets
    snippets = retrieve_snippets(req.attribute)

    # b) Format snippets into a single string for the prompt
    #    e.g. "- snippet one\n- snippet two\n- snippet three"
    context = "\n".join(f"- {s}" for s in snippets)

    formatted_prompt = user_template.format(snippets=context, attribute=req.attribute)
    
    # c) Run the LLMChain
    summary_text = summarization_chain.run(
        attribute=req.attribute,
        snippets=context
    )

    return {
        "summary": summary_text.strip(),
        "snippets": snippets
    }