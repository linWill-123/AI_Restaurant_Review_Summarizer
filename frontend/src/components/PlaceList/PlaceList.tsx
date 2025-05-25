// src/components/PlaceList.tsx
import { useState, useEffect } from "react";
import { transformPlaces, Place } from "../../utils/transformPlaces";

/**
 * PlaceList is a React component that takes a query string as a prop and
 * displays a list of places that match the query. When a place is selected,
 * it renders a message indicating which place was selected.
 *
 * Props:
 *   query: string - the search query to send to the API.
 *
 * State:
 *   places: Place[] - the list of places that match the query.
 *   selected: Place | null - the currently selected place, or null.
 *
 * Side effects:
 *   When the component mounts, it fetches the list of places from the API
 *   and stores them in the "places" state. When the user selects a place,
 *   it updates the "selected" state.
 *
 *   The component re-renders whenever the "places" or "selected" state
 *   changes.
 */
export function PlaceList({
  query,
  onSelectPlace,
}: {
  query: string;
  onSelectPlace: (place: Place) => void;
}) {
  const [places, setPlaces] = useState<Place[]>([]);
  const [selected, setSelected] = useState<Place | null>(null);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/places/?query=${encodeURIComponent(
            query
          )}`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const raw = await response.json();
        setPlaces(transformPlaces(raw));
      } catch (error) {
        console.error("Error fetching places:", error); // Log any errors
      }
    };

    fetchPlaces();
  }, [query]);

  return (
    <>
      <ul>
        {places.map((p) => (
          <button
            key={p.place_id}
            style={{
              cursor: "pointer",
              fontWeight: p === selected ? "bold" : "normal",
            }}
            onClick={() => {
              setSelected(p);
              onSelectPlace(p);
            }}
          >
            {p.name} — {p.rating} ★
          </button>
        ))}
      </ul>
      {selected && (
        <p>
          Selected: {selected.name} ({selected.address})
        </p>
      )}
    </>
  );
}
