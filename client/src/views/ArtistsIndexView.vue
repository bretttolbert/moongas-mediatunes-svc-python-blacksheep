<script setup lang="ts">
import { computed } from 'vue'
import type { LocationQueryRaw } from 'vue-router'
import ByGenreLinks from '../components/ByGenreLinks.vue'
import ByYearRangeAndGenreLinks from '../components/ByYearRangeAndGenreLinks.vue'
import { configState } from '../configStore'
import {
  ARTIST_CITY_LINKS,
  ARTIST_COUNTRY_LINKS,
  ARTIST_LANGUAGE_LINKS,
  ARTIST_REGION_LINKS,
  type GeoQuickLink,
} from '../data/geoLinks'

/** Port of artists_index.html. */
const presentYear = computed(() => configState.config?.presentYear ?? new Date().getFullYear())

const yearRanges: [number, number][] = [
  [2020, 2029],
  [2010, 2019],
  [2000, 2009],
  [1990, 1999],
  [1980, 1989],
  [1970, 1979],
  [1960, 1969],
]

const years = computed(() => {
  const ret: number[] = []
  for (let y = presentYear.value; y >= 1950; y--) ret.push(y)
  return ret
})

/** All artist quick-links sort by count (as in the template). */
function withSort(link: GeoQuickLink): LocationQueryRaw {
  return { sort: 'count', ...link.query }
}
</script>

<template>
  <div>
    <table class="w-100">
      <tr>
        <th>All Artists</th>
      </tr>
      <tr>
        <td>
          <router-link :to="{ path: '/artists', query: { sort: 'count' } }"
            >all artists (sorted by count)</router-link
          >
        </td>
      </tr>
      <tr>
        <td>
          <router-link :to="{ path: '/artists', query: { sort: 'name' } }"
            >all artists (sorted by name)</router-link
          >
        </td>
      </tr>
      <tr>
        <td><router-link to="/artists-cloud">artists word cloud</router-link></td>
      </tr>
    </table>
    <table class="w-100">
      <tr>
        <th>Artists by Country</th>
      </tr>
      <tr v-for="link in ARTIST_COUNTRY_LINKS" :key="link.label">
        <td>
          <router-link :to="{ path: '/artists', query: withSort(link) }">{{ link.label }}</router-link>
        </td>
      </tr>
      <tr>
        <td><router-link to="/artist-countries">[View All Countries]</router-link></td>
      </tr>
      <tr>
        <td>
          <a
            href="/assets/projects/mapgraph/mapgraph.php?map=world&mode=graph&dataset=mediaserver-artist-country-counts&dataitem=ARTIST.COUNT"
            >[View Interactive Map (World of Music)]</a
          >
        </td>
      </tr>
    </table>
    <table class="w-100">
      <tr>
        <th>Artists by Region</th>
      </tr>
      <tr v-for="link in ARTIST_REGION_LINKS" :key="link.label">
        <td>
          <router-link :to="{ path: '/artists', query: withSort(link) }">{{ link.label }}</router-link>
        </td>
      </tr>
      <tr>
        <td><router-link to="/artist-regions">[View All Regions]</router-link></td>
      </tr>
      <tr>
        <td>
          <a
            href="/assets/projects/mapgraph/mapgraph.php?map=us-states&mode=graph&dataset=mediaserver-artist-us-state-counts&dataitem=ARTIST.COUNT"
            >[View Interactive Map (United States of Music)]</a
          >
        </td>
      </tr>
    </table>
    <table class="w-100">
      <tr>
        <th>Artists by City</th>
      </tr>
      <tr v-for="link in ARTIST_CITY_LINKS" :key="link.label">
        <td>
          <router-link :to="{ path: '/artists', query: withSort(link) }">{{ link.label }}</router-link>
        </td>
      </tr>
      <tr>
        <td><router-link to="/artist-cities">[View All Cities]</router-link></td>
      </tr>
    </table>
    <table class="w-100">
      <tr>
        <th>Artists by language</th>
      </tr>
      <tr v-for="link in ARTIST_LANGUAGE_LINKS" :key="link.label">
        <td>
          <router-link :to="{ path: '/artists', query: withSort(link) }">{{ link.label }}</router-link>
        </td>
      </tr>
      <tr>
        <td><router-link to="/artist-languages">[View All Languages]</router-link></td>
      </tr>
    </table>
    <table class="w-100">
      <tr>
        <th>Artists by year range</th>
      </tr>
      <tr v-for="[minYear, maxYear] in yearRanges" :key="`${minYear}-${maxYear}`">
        <td>
          <router-link
            :to="{
              path: '/artists',
              query: { sort: 'count', minYear: String(minYear), maxYear: String(maxYear) },
            }"
            >artists {{ minYear }}-{{ maxYear }}</router-link
          >
        </td>
      </tr>
    </table>
    <ByGenreLinks index-type="artists" />
    <ByYearRangeAndGenreLinks index-type="artists" />
    <table class="w-100">
      <tr>
        <th>Artists by year</th>
      </tr>
      <tr v-for="year in years" :key="year">
        <td>
          <router-link :to="{ path: '/artists', query: { sort: 'count', year: String(year) } }"
            >artists {{ year }}</router-link
          >
        </td>
      </tr>
    </table>
  </div>
</template>
