/**
 * Hardcoded artist geo quick-links, ported from artists_index.html.
 */

export interface GeoQuickLink {
  label: string
  query: Record<string, string | string[]>
}

export const EUROPE_COUNTRY_CODES: string[] = [
  'AL', 'AD', 'AM', 'AT', 'AZ', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI',
  'FR', 'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'KZ', 'XK', 'LV', 'LI', 'LT', 'LU', 'MT',
  'MD', 'MC', 'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 'ES',
  'SE', 'CH', 'TR', 'UA', 'GB', 'VA', 'AX', 'FO', 'GI', 'GG', 'IM', 'JE', 'SJ',
]

export const AFRICA_COUNTRY_CODES: string[] = [
  'AO', 'BF', 'BI', 'BJ', 'BW', 'CD', 'CF', 'CG', 'CI', 'CM', 'CV', 'DJ', 'DZ', 'EG', 'ER',
  'ET', 'GA', 'GH', 'GM', 'GN', 'GQ', 'GW', 'KE', 'KM', 'LR', 'LS', 'LY', 'MA', 'MG', 'ML',
  'MR', 'MU', 'MW', 'MZ', 'NA', 'NE', 'NG', 'RW', 'SC', 'SD', 'SL', 'SN', 'SO', 'SS', 'ST',
  'SZ', 'TD', 'TG', 'TN', 'TZ', 'UG', 'ZA', 'ZM', 'ZW',
]

export const ARTIST_COUNTRY_LINKS: GeoQuickLink[] = [
  { label: 'United States', query: { countryCode: 'US' } },
  { label: 'United Kingdom', query: { countryCode: 'GB' } },
  { label: 'Mexico', query: { countryCode: 'MX' } },
  { label: 'Canada', query: { countryCode: 'CA' } },
  { label: 'France', query: { countryCode: 'FR' } },
  { label: 'Australia', query: { countryCode: 'AU' } },
  { label: 'Germany', query: { countryCode: 'DE' } },
  { label: 'Europe', query: { countryCode: EUROPE_COUNTRY_CODES } },
  { label: 'Africa', query: { countryCode: AFRICA_COUNTRY_CODES } },
]

export const ARTIST_REGION_LINKS: GeoQuickLink[] = [
  { label: 'California, United States', query: { regionCode: 'US-CA' } },
  { label: 'New York, United States', query: { regionCode: 'US-NY' } },
  { label: 'London (metropolitan area), England, United Kingdom', query: { regionCode: 'GB-LND' } },
  { label: 'West Midlands (region), England, United Kingdom', query: { regionCode: 'GB-WMD' } },
  { label: 'Texas, United States', query: { regionCode: 'US-TX' } },
  { label: 'Georgia, United States', query: { regionCode: 'US-GA' } },
  { label: 'Alabama, United States', query: { regionCode: 'US-AL' } },
  { label: 'Québec, Canada', query: { regionCode: 'CA-QC' } },
]

export const ARTIST_CITY_LINKS: GeoQuickLink[] = [
  { label: 'London (London, United Kingdom)', query: { city: 'London' } },
  { label: 'New York City (New York, United States)', query: { city: 'New York City' } },
  { label: 'Los Angeles (California, United States)', query: { city: 'Los Angeles' } },
  { label: 'Chicago (Illinois, United States)', query: { city: 'Chicago' } },
  { label: 'San Francisco (California, United States)', query: { city: 'San Francisco' } },
  { label: 'Paris (Île-de-France, France)', query: { city: 'Paris' } },
  { label: 'Montréal (Québec, Canada)', query: { city: 'Montréal' } },
  { label: 'Atlanta (Georgia, United States)', query: { city: 'Atlanta' } },
  { label: 'Huntsville (Alabama, United States)', query: { city: 'Huntsville' } },
  { label: 'Birmingham (Alabama, United States)', query: { city: 'Birmingham', countryCode: 'US' } },
  { label: 'Birmingham (West Midlands, United Kingdom)', query: { city: 'Birmingham', countryCode: 'GB' } },
]

export const ARTIST_LANGUAGE_LINKS: GeoQuickLink[] = [
  { label: 'English', query: { languageCode: 'en' } },
  { label: 'Spanish', query: { languageCode: 'es' } },
  { label: 'French', query: { languageCode: 'fr' } },
  { label: 'German', query: { languageCode: 'de' } },
]
