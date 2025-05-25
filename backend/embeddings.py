from sentence_transformers import SentenceTransformer

# Load model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str], batch_size: int = 64) -> list[list[float]]:
    """
    Encodes a list of text snippets into embeddings.
    Returns a list of float vectors.
    """
    # model.encode returns numpy array; convert to list of lists
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings.tolist()