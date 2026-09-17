<script setup lang="ts">
import { computed } from 'vue'
import { configState } from '../configStore'

/** Port of player_index.html (shuffle quick-links). */
const presentYear = computed(() => configState.config?.presentYear ?? new Date().getFullYear())

interface ShuffleLink {
  label: string
  query: Record<string, string | string[]>
}

const workoutGenres = [
  'Industrial Metal',
  'Punk',
  'Punk Rock',
  'Heavy Metal',
  'Hip Hop',
  'Urbano',
  'Thrash Metal',
  'Nu Metal',
  'Rock en español',
  'Funk Metal',
  'Hip-Hop français',
]

const links = computed<ShuffleLink[]>(() => {
  const py = presentYear.value
  const ret: ShuffleLink[] = [
    { label: 'shuffle all', query: { minYear: '1960', maxYear: String(py) } },
    {
      label: 'shuffle workout',
      query: { minYear: '1960', maxYear: String(py), genre: workoutGenres },
    },
  ]
  const ranges: [number, number][] = [
    [2020, 2034],
    [2010, 2024],
    [2000, 2014],
    [1990, 2004],
    [1980, 1994],
    [1970, 1984],
    [1960, 1974],
  ]
  for (const [minYear, maxYear] of ranges) {
    ret.push({
      label: `shuffle ${minYear}-${maxYear}`,
      query: { minYear: String(minYear), maxYear: String(maxYear) },
    })
  }
  return ret
})

const years = computed(() => {
  const ret: number[] = []
  for (let y = presentYear.value; y >= 1950; y--) ret.push(y)
  return ret
})
</script>

<template>
  <div>
    <table class="w-100">
      <tr v-for="link in links" :key="link.label">
        <td>
          <router-link :to="{ path: '/player', query: link.query }">{{ link.label }}</router-link>
        </td>
      </tr>
      <tr v-for="year in years" :key="year">
        <td>
          <router-link :to="{ path: '/player', query: { year: String(year) } }"
            >shuffle {{ year }}</router-link
          >
        </td>
      </tr>
    </table>
  </div>
</template>
