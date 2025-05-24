import json
import googlemaps
from config import GOOGLE_MAPS_API_KEY

client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def fetch_reviews(place_id: str):
    details = client.place(place_id=place_id, fields=["reviews"])
    return details.get("result", {}).get("reviews", [])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--place_id", required=True)
    args = parser.parse_args()

    reviews = fetch_reviews(args.place_id)
    out_dir = "data/raw_reviews"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{args.place_id}.json"
    with open(out_path, "w") as f:
        json.dump(reviews, f, indent=2)
    print(f"Saved {len(reviews)} reviews to {out_path}")