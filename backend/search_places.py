import json
import googlemaps
from config import GOOGLE_MAPS_API_KEY

client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def search_places(query: str, location: str = None, radius: int = None):
    params = {"query": query}
    if location:
        params.update({"location": location, "radius": radius})
    results = client.places(query=params["query"], location=params.get("location"), radius=params.get("radius"))
    return results.get("results", [])

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--location", help="lat,lng format")
    parser.add_argument("--radius", type=int, help="in meters")
    args = parser.parse_args()

    places = search_places(args.query, args.location, args.radius)
    out_dir = "data/place_search"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{args.query.replace(' ', '_')}.json"
    with open(out_path, "w") as f:
        json.dump(places, f, indent=2)
    print(f"Saved {len(places)} places to {out_path}")