/**
 * Shared types mirroring the Flask JSON API payloads
 * (see app/api/routes.py).
 */

export interface MediaFile {
  path: string
  size: number
  format: string
  title: string
  artist: string
  albumartist: string
  album: string
  genre: string
  year: number
  duration: number
  countryCode: string
  regionCode: string
  city: string
  languageCode: string
}

export interface AlbumInfo {
  artist: string
  album: string
  year: number
  coverPath: string
}

export interface ArtistCount {
  name: string
  count: number
}

export interface GenreCount {
  genre: string
  count: number
}

export interface ArtistInfo {
  name: string
  countryCode: string
  regionCode: string
  city: string
  languageCode: string
}

export interface GeoCountItem {
  /** User-facing criteria name, e.g. "Country" */
  name: string
  /** User-facing value, e.g. "United States" or "Huntsville (Alabama, United States)" */
  value: string
  /** Filter criteria usable as router query params, e.g. { countryCode: "US" } */
  criteria: Record<string, string>
  count: number
}

export interface WebSearchPlaybackMethod {
  name: string
  searchQueryUrlFormat: string
}

export interface ServerConfig {
  playbackMethodLocalEnabled: boolean
  webSearchPlaybackMethods: WebSearchPlaybackMethod[]
  ageVerification: boolean
  limitBandwidth: boolean
  maxResults: number
  maxResultsAlbumCovers: number
  presentYear: number
}

/** A single random track (player). */
export interface TrackInfo {
  path: string
  coverPath: string
  artist: string
  album: string
  title: string
  genre: string
  year: number
  countryCode: string
  regionCode: string
  city: string
  languageCode: string
}

export interface WordCloudWord {
  text: string
  size?: number
}

export type GeoKind = 'countries' | 'regions' | 'cities' | 'languages'

export type WordCloudType = 'genre' | 'artist'
