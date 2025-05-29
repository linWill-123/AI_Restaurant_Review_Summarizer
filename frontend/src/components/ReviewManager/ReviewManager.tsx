// src/components/ReviewManager.tsx
import { useState } from "react";
import { cleanReviews } from "../../utils/cleanReviews";

export function ReviewManager({ placeId }: { placeId: string }) {
  const [snippets, setSnippets] = useState<string[]>([]);
  const [indexedCount, setIndexedCount] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  /** Fetch raw reviews, clean & chunk them, store in snippets state */
  const loadReviews = async () => {
    setLoading(true);
    try {
      const raw = await fetch(
        `${import.meta.env.VITE_API_URL}/reviews/${placeId}`
      ).then((r) => r.json());
      console.log("Raw reviews:", raw);
      setSnippets(cleanReviews(raw));
    } finally {
      setLoading(false);
    }
  };

  /** Send cleaned snippets to backend for embedding & indexing */
  const confirmAndIndex = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/index_reviews/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ place_id: placeId, snippets }),
        }
      );
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const data = await res.json();
      setIndexedCount(data.indexed_count);
    } catch (err) {
      console.error("Indexing failed", err);
      alert("Failed to index snippets. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <button
        onClick={loadReviews}
        disabled={loading}
        className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        {loading ? "Loading…" : "Load Reviews"}
      </button>

      {snippets.length > 0 && (
        <>
          <p>Preview snippets (first 100 chars):</p>
          <ul className="list-disc pl-5 space-y-1 max-h-48 overflow-auto">
            {snippets.map((s, i) => (
              <li key={i}>{s.slice(0, 100)}…</li>
            ))}
          </ul>
          <button
            onClick={confirmAndIndex}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {loading ? "Indexing…" : "Confirm & Index"}
          </button>
        </>
      )}

      {indexedCount !== null && (
        <p className="text-green-700">
          ✅ Successfully indexed {indexedCount} snippet
          {indexedCount > 1 ? "s" : ""}.
        </p>
      )}
    </div>
  );
}
