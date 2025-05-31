// src/components/ReviewManager.tsx
import { useState, ChangeEvent } from "react";
import { cleanReviews } from "../../utils/cleanReviews";

type FeatureOption =
  | "food quality"
  | "service"
  | "price"
  | "environment"
  | "custom";

export function ReviewManager({ placeId }: { placeId: string }) {
  const [snippets, setSnippets] = useState<string[]>([]);
  const [indexedCount, setIndexedCount] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  // New state for feature selection & summary
  const [featureOption, setFeatureOption] =
    useState<FeatureOption>("food quality");

  const [customFeature, setCustomFeature] = useState("");
  const [summary, setSummary] = useState<string | null>(null);
  const [summarizing, setSummarizing] = useState(false);

  /** Fetch raw reviews, clean & chunk them, store in snippets state */
  const loadReviews = async () => {
    setLoading(true);
    try {
      const raw = await fetch(
        `${import.meta.env.VITE_API_URL}/reviews/${placeId}`
      ).then((r) => r.json());
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

  /** Send selected feature to backend summarization endpoint */
  const summarizeFeature = async () => {
    const attr =
      featureOption === "custom" && customFeature.trim()
        ? customFeature.trim()
        : featureOption;

    if (!attr) {
      alert("Please enter a custom feature or select one from the list.");
      return;
    }

    setSummarizing(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/summarize/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attribute: attr, k: 5 }),
      });
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const data = await res.json();
      setSummary(data.summary);
    } catch (err) {
      console.error("Summarization failed", err);
      alert("Failed to summarize. Check console for details.");
    } finally {
      setSummarizing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* 1) Load Reviews Button */}
      <button
        onClick={loadReviews}
        disabled={loading}
        className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        {loading ? "Loading…" : "Load Reviews"}
      </button>

      {/* 2) Preview & Index */}
      {snippets.length > 0 && indexedCount === null && (
        <div className="space-y-4">
          <p className="font-semibold">Preview snippets (first 100 chars):</p>
          <ul className="list-disc pl-5 space-y-1 max-h-48 overflow-auto border p-2 rounded">
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
        </div>
      )}

      {/* 3) Confirmation message after indexing */}
      {indexedCount !== null && (
        <p className="text-green-700">
          ✅ Successfully indexed {indexedCount} snippet
          {indexedCount > 1 ? "s" : ""}.
        </p>
      )}

      {/* 4) Feature selection and summarize button */}
      {indexedCount !== null && (
        <div className="space-y-4 border-t pt-4">
          <p className="font-semibold">Choose a feature to summarize:</p>
          <div className="flex flex-col space-y-2">
            {/* Radio buttons for predefined features */}
            {["food quality", "service", "price", "environment"].map((opt) => (
              <label key={opt} className="flex items-center space-x-2">
                <input
                  type="radio"
                  name="feature"
                  value={opt}
                  checked={featureOption === opt}
                  onChange={() => setFeatureOption(opt as FeatureOption)}
                  className="form-radio"
                />
                <span className="capitalize">{opt}</span>
              </label>
            ))}

            {/* Custom feature option */}
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                name="feature"
                value="custom"
                checked={featureOption === "custom"}
                onChange={() => setFeatureOption("custom")}
                className="form-radio"
              />
              <span>Custom:</span>
              <input
                type="text"
                value={customFeature}
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  setCustomFeature(e.target.value)
                }
                disabled={featureOption !== "custom"}
                placeholder="Enter custom feature"
                className="ml-2 p-1 border rounded disabled:bg-gray-100"
              />
            </label>
          </div>

          {/* Summarize button */}
          <button
            onClick={summarizeFeature}
            disabled={summarizing}
            className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
          >
            {summarizing ? "Summarizing…" : "Get Summary"}
          </button>
        </div>
      )}

      {/* 5) Display the summary */}
      {summary && (
        <div className="mt-4 p-4 bg-gray-50 border rounded">
          <h3 className="text-lg font-semibold mb-2">Summary:</h3>
          <ul className="list-disc pl-5 space-y-1">
            {summary.split("\n").map((sentence, index) => (
              <li key={index}>{sentence.trim()}.</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
