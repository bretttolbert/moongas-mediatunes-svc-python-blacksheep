<script setup lang="ts">
import { computed } from 'vue'
import ByGenreLinks from '../components/ByGenreLinks.vue'
import ByYearRangeAndGenreLinks from '../components/ByYearRangeAndGenreLinks.vue'
import { configState } from '../configStore'

/** Port of albums_index.html (also served at "/"). */
const presentYear = computed(() => configState.config?.presentYear ?? new Date().getFullYear())
const limitBandwidth = computed(() => configState.config?.limitBandwidth ?? true)

const yearRanges: [number, number][] = [
  [2020, 2029],
  [2015, 2019],
  [2010, 2014],
  [2005, 2009],
  [2000, 2004],
  [1995, 1999],
  [1990, 1994],
  [1985, 1989],
  [1980, 1984],
  [1970, 1975],
  [1970, 1974],
  [1960, 1969],
  [1950, 1959],
  [1940, 1949],
]

const years = computed(() => {
  const ret: number[] = []
  for (let y = presentYear.value; y >= 1950; y--) ret.push(y)
  return ret
})
</script>

<template>
  <div>
    <table v-if="!limitBandwidth" class="w-100">
      <tr>
        <th>All Albums</th>
      </tr>
      <tr>
        <td><router-link to="/albums">all albums</router-link></td>
      </tr>
    </table>
    <table class="w-100">
      <tr>
        <th>Albums by year range</th>
      </tr>
      <tr v-for="[minYear, maxYear] in yearRanges" :key="`${minYear}-${maxYear}`">
        <td>
          <router-link
            :to="{ path: '/albums', query: { minYear: String(minYear), maxYear: String(maxYear) } }"
            >albums {{ minYear }}-{{ maxYear }}</router-link
          >
        </td>
      </tr>
    </table>
    <ByGenreLinks index-type="albums" />
    <ByYearRangeAndGenreLinks index-type="albums" />
    <table class="w-100">
      <tr>
        <th>Albums by year</th>
      </tr>
      <tr v-for="year in years" :key="year">
        <td>
          <router-link :to="{ path: '/albums', query: { year: String(year) } }"
            >albums {{ year }}</router-link
          >
        </td>
      </tr>
    </table>
  </div>
</template>
