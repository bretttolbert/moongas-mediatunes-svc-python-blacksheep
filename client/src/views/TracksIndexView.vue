<script setup lang="ts">
import { computed } from 'vue'
import { configState } from '../configStore'

/** Port of tracks_index.html. */
const presentYear = computed(() => configState.config?.presentYear ?? new Date().getFullYear())

const yearRanges: [number, number][] = [
  [2015, 2025],
  [2000, 2015],
  [1990, 1999],
  [1980, 1989],
  [1970, 1979],
]

const years = computed(() => {
  const ret: number[] = []
  for (let y = presentYear.value; y >= 1950; y--) ret.push(y)
  return ret
})
</script>

<template>
  <div>
    <table class="w-100">
      <tr v-for="[minYear, maxYear] in yearRanges" :key="`${minYear}-${maxYear}`">
        <td>
          <router-link
            :to="{ path: '/tracks', query: { minYear: String(minYear), maxYear: String(maxYear) } }"
            >tracks year range {{ minYear }}-{{ maxYear }}</router-link
          >
        </td>
      </tr>
    </table>
    <table class="w-100">
      <tr v-for="year in years" :key="year">
        <td>
          <router-link :to="{ path: '/tracks', query: { year: String(year) } }"
            >tracks {{ year }}</router-link
          >
        </td>
      </tr>
    </table>
  </div>
</template>
