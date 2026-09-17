/**
 * Port of the Jinja `result_or_results` filters from app/__init__.py:
 * "1,234+ results" / "1 result".
 */
export function formatResults(count: number, maxResults: number): string {
  const plus = count >= maxResults ? '+' : ''
  const noun = count === 1 ? 'result' : 'results'
  return `${count.toLocaleString('en-US')}${plus} ${noun}`
}

/** Format a web-search playback URL by substituting track metadata. */
export function formatSearchQueryUrl(
  searchQueryUrlFormat: string,
  artist: string,
  album: string,
  title: string,
): string {
  return searchQueryUrlFormat
    .replaceAll('{artist}', encodeURIComponent(artist))
    .replaceAll('{album}', encodeURIComponent(album))
    .replaceAll('{title}', encodeURIComponent(title))
}
