import type { LocationQuery } from 'vue-router'
import type {
  AlbumInfo,
  ArtistCount,
  ArtistInfo,
  GeoCountItem,
  GeoKind,
  GenreCount,
  MediaFile,
  ServerConfig,
  TrackInfo,
  WordCloudWord,
} from './types'

/**
 * Serialize vue-router query params into URLSearchParams.
 * Multi-value params are repeated (?genre=a&genre=b), matching what
 * Flask's request.args.getlist() expects on the backend.
 */
export function buildSearchParams(query: LocationQuery): URLSearchParams {
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(query)) {
    if (value === null || value === undefined || value === '') continue
    if (Array.isArray(value)) {
      for (const v of value) {
        if (v !== null && v !== undefined && v !== '') params.append(key, v)
      }
    } else {
      params.append(key, value)
    }
  }
  return params
}

async function fetchJson<T>(path: string, query?: LocationQuery): Promise<T> {
  const qs = query ? buildSearchParams(query).toString() : ''
  const url = qs ? `${path}?${qs}` : path
  const resp = await fetch(url)
  if (!resp.ok) {
    throw new Error(`GET ${url} failed: ${resp.status} ${resp.statusText}`)
  }
  return (await resp.json()) as T
}

/** URL for the Flask /getfile/<path> media-file endpoint. */
export function getfileUrl(path: string): string {
  return `/getfile${path.startsWith('/') ? path : `/${path}`}`
}

export const api = {
  config: () => fetchJson<ServerConfig>('/api/config'),

  albums: (query: LocationQuery) =>
    fetchJson<{ albums: AlbumInfo[] }>('/api/albums', query),

  tracks: (query: LocationQuery) =>
    fetchJson<{ files: MediaFile[]; coverPath: string }>('/api/tracks', query),

  artists: (query: LocationQuery) =>
    fetchJson<{ artists: ArtistCount[] }>('/api/artists', query),

  artist: (query: LocationQuery) => fetchJson<{ artist: ArtistInfo }>('/api/artist', query),

  genres: (sort?: string) =>
    fetchJson<{ genres: GenreCount[] }>('/api/genres', sort ? { sort } : undefined),

  artistGeo: (kind: GeoKind) => fetchJson<{ items: GeoCountItem[] }>(`/api/artist-geo/${kind}`),

  wordCloudGenres: () => fetchJson<{ words: WordCloudWord[] }>('/api/wordcloud/genres'),

  wordCloudArtists: (query: LocationQuery) =>
    fetchJson<{ words: WordCloudWord[] }>('/api/wordcloud/artists', query),

  randomTrack: (query: LocationQuery) => fetchJson<TrackInfo>('/api/random-track', query),
}
