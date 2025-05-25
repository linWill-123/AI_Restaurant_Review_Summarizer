// src/utils/cleanReviews.ts
/**
 * Take raw review objects, strip HTML/emojis, lowercase, whitespace-normalize,
 * then chunk into <=512-token segments with 50-token overlap.
 */
export function cleanReviews(raw: any[]): string[] {
  const maxLen = 512;
  const overlap = 50;

  return raw.flatMap((r) => {
    // 1) Remove HTML tags & non-ASCII, collapse whitespace, lowercase
    const txt = r.text
      .replace(/<[^>]+>/g, " ")
      .replace(/[^\x00-\x7F]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();

    const tokens = txt.split(" ");
    if (tokens.length <= maxLen) {
      return [txt];
    }

    // 2) Slice into overlapping windows
    const chunks: string[] = [];
    for (let i = 0; i < tokens.length; i += maxLen - overlap) {
      chunks.push(tokens.slice(i, i + maxLen).join(" "));
    }
    return chunks;
  });
}
