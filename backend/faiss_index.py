import faiss
import numpy as np

class FaissIndex:
    def __init__(self, dim: int, use_gpu: bool = False):
        self.dim = dim
        # Choose Flat or HNSW index
        self.index = faiss.IndexHNSWFlat(dim, 32) if not use_gpu else self._to_gpu(faiss.IndexFlatL2(dim))

    def _to_gpu(self, cpu_index):
        # Optional: move to GPU if available
        res = faiss.StandardGpuResources()
        return faiss.index_cpu_to_gpu(res, 0, cpu_index)

    def reset(self):
        self.index.reset()

    def add_embeddings(self, embeddings: list[list[float]]):
        arr = np.array(embeddings, dtype='float32')
        self.index.add(arr)

    def search(self, query_emb: list[float], k: int = 2):
        arr = np.array([query_emb], dtype='float32')
        distances, indices = self.index.search(arr, k)
        return distances[0].tolist(), indices[0].tolist()

# Example usage
if __name__ == '__main__':
    # dim must match embedding size, e.g. 384 for all-MiniLM-L6-v2
    idx = FaissIndex(dim=384)
    dummy_embs = np.random.random((100, 384)).astype('float32')
    idx.add_embeddings(dummy_embs.tolist())
    q = dummy_embs[0]
    d, i = idx.search(q, k=5)
    print("Distances:", d)
    print("Indices:", i)