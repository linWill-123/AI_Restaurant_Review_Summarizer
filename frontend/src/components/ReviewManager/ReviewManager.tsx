// src/components/ReviewManager.tsx
import { useState } from "react";
import { cleanReviews } from "../../utils/cleanReviews";

export function ReviewManager({ placeId }: { placeId: string }) {
  const [snippets, setSnippets] = useState<string[]>([]);
  const [confirmed, setConfirmed] = useState(false);

  /**
   * Fetches raw reviews for the given placeId from the API, cleans the reviews
   * by removing HTML/emojis and chunking them into segments, and updates the
   * snippets state with the cleaned review snippets.
   */

  const loadReviews = async () => {
    const raw = await fetch(
      `${import.meta.env.VITE_API_URL}/reviews/${placeId}`
    ).then((r) => r.json());
    setSnippets(cleanReviews(raw));
  };

  const confirmAndIndex = () => {
    // e.g. call your backend to embed & upsert these snippets
    fetch("/api/indexSnippets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ placeId, snippets }),
    }).then(() => setConfirmed(true));
  };

  return (
    <div>
      <button onClick={loadReviews}>Load Reviews</button>

      {snippets.length > 0 && !confirmed && (
        <>
          <p>Preview snippets (first 100 chars):</p>
          <ul>
            {snippets.map((s, i) => (
              <li key={i}>{s.slice(0, 100)}…</li>
            ))}
          </ul>
          <button onClick={confirmAndIndex}>Confirm & Index</button>
        </>
      )}

      {confirmed && <p>✅ Snippets confirmed and sent to be indexed.</p>}
    </div>
  );
}
