from faiss_index import FaissIndex

# Initialize the Faiss index
faiss_idx = FaissIndex(dim=384, use_gpu=False)

# Store all snippets in memory for indexing
all_snippets: list[str] = []