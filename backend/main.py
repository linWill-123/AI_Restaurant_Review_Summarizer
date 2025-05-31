from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from search_places import search_places
from fetch_reviews import fetch_reviews
from embeddings import embed_texts
from faiss_index import FaissIndex
from pydantic import BaseModel

from langchain import LLMChain
from langchain.llms import OpenAI

from prompts import prompt as summarization_prompt

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the Faiss index with the embedding dimension, used and shared across endpoints
faiss_idx = FaissIndex(dim=384, use_gpu=False)

# Store all snippets in memory for indexing
all_snippets: list[str] = []

# Intialize the LLMChain 
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
prompt = PromptTemplate(
    input_variables=["attribute", "snippets"],
    template=system_prompt + "\n\n" + user_template
)
summarization_chain = LLMChain(llm=llm, prompt=summarization_prompt)

class SummarizeRequests(BaseModel):
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
    snippets = retrieve_snippets(req.attribute, k=req.k)

    # b) Format snippets into a single string for the prompt
    #    e.g. "- snippet one\n- snippet two\n- snippet three"
    context = "\n".join(f"- {s}" for s in snippets)

    # c) Run the LLMChain
    summary_text = summarization_chain.run(
        attribute=req.attribute,
        snippets=context
    )

    return {
        "summary": summary_text.strip(),
        "snippets": snippets
    }