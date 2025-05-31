from embeddings import embed_texts
from faiss_index import FaissIndex

# Ensure FAISS index is initialized and populated elsewhere (e.g. in main.py)
# Here, we import the global index instance
from main import faiss_idx

def retrieve_snippets(query: str, k: int = 5) -> list[str]:
    """
    Given a text query, embed it and return the top-k raw review snippets.
    """
    # 1. Embed the query
    query_emb = embed_texts([query])[0]
    # 2. Search FAISS
    distances, indices = faiss_idx.search(query_emb, k)
    # 3. Map indices to stored snippet texts
    # Assume you maintain a parallel list `all_snippets` in main.py
    from main import all_snippets  # list[str]
    return [all_snippets[i] for i in indices]