// src/App.tsx
import { useState } from "react";
import "./App.css";
import { PlaceList } from "./components/PlaceList";
import { ReviewManager } from "./components/ReviewManager";

function App() {
  const [query, setQuery] = useState("");
  const [searchTerm, setSearchTerm] = useState<string | null>(null);
  const [selectedPlaceId, setSelectedPlaceId] = useState<string | null>(null);

  const onSearch = () => {
    // trim and avoid empty
    const q = query.trim();
    if (q) {
      setSearchTerm(q);
      setSelectedPlaceId(null); // reset selection when new search
    }
  };

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Review Summarizer</h1>

      {/* Search input */}
      <div className="flex mb-6">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. pizza near me"
          className="flex-1 p-2 border rounded-l"
        />
        <button
          onClick={onSearch}
          className="px-4 bg-blue-600 text-white rounded-r hover:bg-blue-700"
        >
          Search
        </button>
      </div>

      {/* Place list */}
      {searchTerm && (
        <div className="mb-6">
          <h2 className="text-xl mb-2">Results for “{searchTerm}”:</h2>
          <PlaceList
            query={searchTerm}
            onSelectPlace={(place) => setSelectedPlaceId(place.place_id)}
          />
        </div>
      )}

      {/* Review manager for selected place */}
      {selectedPlaceId && (
        <div className="mb-6">
          <h2 className="text-xl mb-2">Reviews for selected place:</h2>
          <ReviewManager placeId={selectedPlaceId} />
        </div>
      )}
    </div>
  );
}

export default App;
