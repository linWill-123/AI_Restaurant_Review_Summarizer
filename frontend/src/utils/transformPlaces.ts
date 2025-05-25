// src/utils/transformPlaces.ts
export interface Place {
  place_id: string;
  name: string;
  address: string;
  lat: number;
  lng: number;
  rating: number;
  user_ratings_total: number;
  photo_reference: string | null;
}

/**
 * Map raw Google Places response into our minimal Place schema.
 */
export function transformPlaces(raw: any[]): Place[] {
  return raw.map((p) => ({
    place_id: p.place_id,
    name: p.name,
    address: p.formatted_address,
    lat: p.geometry.location.lat,
    lng: p.geometry.location.lng,
    rating: p.rating,
    user_ratings_total: p.user_ratings_total,
    photo_reference: p.photos?.[0]?.photo_reference ?? null,
  }));
}
