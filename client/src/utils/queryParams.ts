import type { LocationQuery } from 'vue-router'

/** All non-empty string values for a (possibly multi-value) query param. */
export function queryList(query: LocationQuery, key: string): string[] {
  const v = query[key]
  if (Array.isArray(v)) return v.filter((x): x is string => typeof x === 'string' && x !== '')
  return typeof v === 'string' && v !== '' ? [v] : []
}

/** First value of a query param, or null. */
export function queryScalar(query: LocationQuery, key: string): string | null {
  const v = query[key]
  if (Array.isArray(v)) return v.find((x) => x !== null && x !== '') ?? null
  return typeof v === 'string' && v !== '' ? v : null
}
